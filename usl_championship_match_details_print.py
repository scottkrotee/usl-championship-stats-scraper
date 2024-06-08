import requests
from bs4 import BeautifulSoup

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

        # Iterate over each table
        for index, stats_table in enumerate(stats_tables):
            # Extract the headers
            headers = [header.text.strip() for header in stats_table.find_all('th')]

            # Initialize a list to hold all the data
            all_data = []

            # Extract each row of statistics
            for row in stats_table.find_all('tr'):  
                # Extract each column of the row
                cols = row.find_all(['th', 'td'])
                cols_data = [ele.text.strip() for ele in cols]
                all_data.append(cols_data)

            # Print the data
            print(f"Data for table {index}:")
            for row in all_data:
                print(row)

    except requests.HTTPError as e:
        print(f'HTTP Error occurred: {e.response.status_code}')
    except requests.RequestException as e:
        print(f'Request exception: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')

# Call the function with the URL
scrape_usl_championship_fixtures(url)
