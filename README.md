## USL Championship Stats Scraper
This Python script is designed to scrape and export statistics from the USL Championship league page on FBRef.com. It captures data from HTML tables under each section and exports them into an Excel file.

## Features
Scrape statistics from USL Championship Stats

Export data into individual sheets within an Excel workbook

Handles different table structures and merges multiple headers

## Prerequisites
Before running this script, ensure you have the following packages installed:

requests for sending HTTP requests.

beautifulsoup4 for parsing HTML content.

pandas for data manipulation and export.

xlsxwriter for creating Excel files.


You can install these packages using pip:


```bash
pip install requests beautifulsoup4 pandas xlsxwriter
```

## Usage
To use this script, simply run the Python file:

```bash
python scrape_usl_championship_stats.py
```

The script will automatically scrape the data from the FBRef USL Championship page and save it as usl_championship_stats.xlsx in the same directory as the script.

## Error Handling
The script includes error handling for HTTP errors and other request issues, providing clear messages to help diagnose problems.

## Contributing
Feel free to fork this project and submit pull requests. You can also open an issue if you find bugs or have feature requests.

## License
This project is open-source and available under the MIT License.
