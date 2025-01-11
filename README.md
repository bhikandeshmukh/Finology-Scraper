
# Web Scraping Script Documentation

## Overview
This Python script performs web scraping to extract financial data from web pages and saves the results in a CSV file. The script uses various libraries for HTTP requests, HTML parsing, and data cleaning.

## Features
- Fetches web pages using random user agents for improved anonymity.
- Extracts key financial metrics such as company name, sector, market capitalization, P/E ratio, and more.
- Handles errors gracefully and skips problematic URLs.
- Displays progress using a terminal-based progress bar (`tqdm`).
- Saves results in a CSV file with structured data.

## Prerequisites
To use this script, you need the following:
- Python 3.6 or later.
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `csv`
  - `tqdm`
  - `random`

Install the libraries using:
```bash
pip install requests beautifulsoup4 tqdm
```

## Files
1. **`urls.txt`**  
   A text file containing the list of URLs to scrape. Each URL should be on a new line.

2. **`scraped_results.csv`**  
   The output file where the scraped data will be saved.

## How to Use
1. **Prepare the URL File:**  
   Create a file named `urls.txt` and list the URLs you want to scrape, one per line.

2. **Run the Script:**  
   Execute the script in a terminal:
   ```bash
   python main.py
   ```

3. **View the Results:**  
   The scraped data will be saved in a file named `scraped_results.csv`.

## Key Components
### 1. Fetching Web Pages
The script fetches pages using the `fetch_page` function. It randomly selects a user agent from a predefined list to mimic browser behavior:
```python
headers = {
    "User-Agent": random.choice(user_agents),
    "Accept-Language": "en-US,en;q=0.5"
}
response = requests.get(url, headers=headers)
```

### 2. Data Extraction
The `extract_data` function parses the HTML content using `BeautifulSoup` to extract specific data points, such as:
- Company Name
- Sector
- Last Traded Price (LTP)
- P/E Ratio
- Market Cap
- And more...

Example:
```python
company_name = soup.find('span', {'id': 'mainContent_ltrlCompName'}).get_text(strip=True)
```

### 3. Data Cleaning
The script includes a utility function `clean_text` to remove unwanted characters (e.g., `₹`) and format the text.

### 4. Progress Tracking
The script uses `tqdm` to display a progress bar, making it easier to track scraping progress:
```python
for url in tqdm(urls, desc="Scraping URLs", unit="url", ncols=100):
```

### 5. Saving Results
The `save_results` function writes the extracted data to a CSV file with structured headers.

## Error Handling
- If a URL fetch fails, the script logs the error and continues with the next URL.
- Extracted fields default to "N/A" if data is missing or inaccessible.

## Example Output
**Sample `scraped_results.csv`:**
| URL                | Company Name | Sector   | LTP  | P/E Ratio | Market Cap (Cr) | ... |
|--------------------|--------------|----------|------|-----------|-----------------|-----|
| example.com/stock1 | ABC Ltd.     | Finance  | 1234 | 20.5      | 5000            | ... |
| example.com/stock2 | XYZ Ltd.     | Pharma   | 5678 | 30.1      | 10000           | ... |

## Notes
- Ensure the URLs provided in `urls.txt` are accessible and formatted correctly.
- Modify the HTML selectors in `extract_data` if the structure of the target web pages changes.

## Conclusion
This script provides a flexible and efficient way to scrape financial data from multiple URLs. Customize it further to suit your specific requirements!
