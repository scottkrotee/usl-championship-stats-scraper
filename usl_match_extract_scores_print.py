### Author: Scott Krotee - 2024 ###

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of website to scrape
url = 'https://fbref.com/en/comps/73/schedule/USL-Championship-Scores-and-Fixtures'

def scrape_usl_championship_fixtures(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all tables on the page
        stats_tables = soup.find_all('table')
        if not stats_tables:
            print("No statistics tables found.")
            return

        # Initialize an empty list to hold the extracted data
        data = []

        # Iterate over each table
        for stats_table in stats_tables:
            # Extract the headers
            headers = [header.text.strip() for header in stats_table.find_all('th')]

            # Find the indices of the desired columns
            home_index = headers.index('Home')
            away_index = headers.index('Away')

            # Extract each row of statistics
            for row in stats_table.find_all('tr')[1:]:  # Skip the header row
                # Extract each column of the row
                cols = row.find_all(['th', 'td'])
                cols_data = [ele.text.strip() for ele in cols]

                # Extract the "Home" and "Away" columns
                home_team = cols_data[home_index]
                away_team = cols_data[away_index]

                # Extract the "Score" from the combined column and split into two scores
                score_with_details = cols_data[home_index + 1]  # Assuming "Score" is right after "Home"
                scores = score_with_details.split('–')  # Split score into home and away scores

                # Check if both home and away scores are present
                if len(scores) == 2:
                    home_score, away_score = scores[0].strip(), scores[1].strip()
                    # Append the extracted data to the list
                    data.append([home_team, away_team, home_score, away_score])

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data, columns=['Home', 'Away', 'Home Score', 'Away Score'])

        return df

    except requests.HTTPError as e:
        print(f'HTTP Error occurred: {e.response.status_code}')
    except requests.RequestException as e:
        print(f'Request exception: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')

# Call the function to scrape the data and create a DataFrame
usl_fixtures_df = scrape_usl_championship_fixtures(url)

# Drop rows with missing scores
usl_fixtures_df.dropna(subset=['Home Score', 'Away Score'], inplace=True)

# Print the DataFrame
print(usl_fixtures_df)
