### Author: Scott Krotee - 2024 ###

import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

# URL of website to scrape
url = 'https://fbref.com/en/comps/73/USL-Championship-Stats'

def scrape_usl_championship_stats(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize an Excel writer
        with pd.ExcelWriter('usl_championship_stats.xlsx', engine='xlsxwriter') as writer:
            # Iterate over each <h2> element
            headers = soup.find_all('h2')
            for header in headers:
                # Start searching from the next element
                current_element = header.next_element
                
                # Loop to skip over any non-table elements
                while current_element and (current_element.name != 'table'):
                    current_element = current_element.next_element

                # Check if we have a table to process
                if current_element and current_element.name == 'table':
                    # Convert the table to a string, wrap in StringIO object
                    table_html = str(current_element)
                    df = pd.read_html(StringIO(table_html))[0]

                    # Flatten MultiIndex if necessary
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = [' '.join(col).strip() for col in df.columns.values]

                    # Use the header text for the sheet name, ensuring it's within Excel's character limit
                    sheet_name = header.text.strip()[:31]

                    # Write DataFrame to a specific sheet
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

    except requests.HTTPError as e:
        print(f'HTTP Error occurred: {e.response.status_code}')
    except requests.RequestException as e:
        print(f'Request exception: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')

# Call the function with the URL
scrape_usl_championship_stats(url)
