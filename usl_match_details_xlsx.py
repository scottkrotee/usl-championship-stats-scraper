### Author: Scott Krotee - Sept 7, 2024 ###

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

        # Find the first table on the page
        stats_table = soup.find('table')
        if not stats_table:
            print("No statistics table found.")
            return

        # Extract the headers
        headers = [header.text.strip() for header in stats_table.find_all('th')]

        # Determine the indices for necessary columns
        week_index = headers.index('Wk') if 'Wk' in headers else None
        day_index = headers.index('Day')
        date_index = headers.index('Date')
        time_index = headers.index('Time')
        home_index = headers.index('Home')
        away_index = headers.index('Away')
        score_index = headers.index('Score')
        att_index = headers.index('Attendance') if 'Attendance' in headers else None
        venue_index = headers.index('Venue')
        ref_index = headers.index('Referee') if 'Referee' in headers else None

        # Initialize an empty list to hold the extracted data
        data = []

        # Extract each row of statistics
        for row in stats_table.find_all('tr')[1:]:  # Skip the header row
            cols = row.find_all(['th', 'td'])
            if len(cols) > home_index:  # Check for a valid row
                # Extract data for each row
                week = cols[week_index].text.strip() if week_index is not None else 'N/A'
                day = cols[day_index].text.strip()
                date = cols[date_index].text.strip()
                time = cols[time_index].text.strip()
                home_team = cols[home_index].text.strip()
                away_team = cols[away_index].text.strip()
                score = cols[score_index].text.strip()
                attendance = cols[att_index].text.strip() if att_index is not None else 'N/A'
                venue = cols[venue_index].text.strip()
                referee = cols[ref_index].text.strip() if ref_index is not None else 'N/A'

                # Split scores
                scores = score.split('–')
                if len(scores) == 2:
                    home_score, away_score = scores[0].strip(), scores[1].strip()
                else:
                    home_score, away_score = None, None  # Handle missing or malformed scores

                # Append the extracted data to the list
                data.append([week, day, date, time, home_team, away_team, home_score, away_score, attendance, venue, referee])

        # Create a DataFrame from the extracted data
        columns = ['Week', 'Day', 'Date', 'Time', 'Home Team', 'Away Team', 'Home Score', 'Away Score', 'Attendance', 'Venue', 'Referee']
        df = pd.DataFrame(data, columns=columns)

        return df

    except requests.HTTPError as e:
        print(f'HTTP Error occurred: {e.response.status_code}')
    except requests.RequestException as e:
        print(f'Request exception: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')

# Call the function to scrape the data and create a DataFrame
usl_fixtures_df = scrape_usl_championship_fixtures(url)

# Check if DataFrame is not empty before proceeding
if usl_fixtures_df is not None and not usl_fixtures_df.empty:
    # Drop rows with missing scores
    usl_fixtures_df.dropna(subset=['Home Score', 'Away Score'], inplace=True)

    # Save the DataFrame to an Excel file
    usl_fixtures_df.to_excel('usl_match_details.xlsx', index=False)

    # Print the DataFrame
    print(usl_fixtures_df)
else:
    print("No data was scraped or DataFrame is empty.")
