import random
import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm  # Import tqdm for the progress bar

# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edge/91.0.864.59",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
]

# Function to get page content using random user agent
def fetch_page(url):
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.5"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None  # Return None if there's an error

# Function to clean up the text (remove ₹ symbol, retain 'Cr.' only if it's part of the text)
def clean_text(text, retain_cr=False):
    if not text:
        return 'N/A'
    
    # Remove ₹ symbol and strip spaces
    cleaned_text = text.replace('₹', '').strip()
    
    # If 'Cr.' is in the original HTML, ensure it is not added again
    if retain_cr and 'Cr.' in text:
        if cleaned_text.endswith('Cr.'):
            return cleaned_text  # If Cr. is already there, don't append it again
        else:
            cleaned_text += ' Cr.'  # Append Cr. only if it's not there already
    
    return cleaned_text

# Function to extract the required information from the page
def extract_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting basic data based on the HTML structure of the page
    company_name = soup.find('span', {'id': 'mainContent_ltrlCompName'}).get_text(strip=True) if soup.find('span', {'id': 'mainContent_ltrlCompName'}) else 'N/A'
    sector = soup.find('a', {'class': 'font-weight-bold'}).get_text(strip=True) if soup.find('a', {'class': 'font-weight-bold'}) else 'N/A'
    ltp = soup.find('span', {'class': 'Number'}).get_text(strip=True) if soup.find('span', {'class': 'Number'}) else 'N/A'

    # Updated P/E Ratio extraction using find_all with the correct index and value attribute
    pe_ratio = clean_text(soup.find_all('td', class_='Number')[3].get('value')) if len(soup.find_all('td', class_='Number')) > 3 else 'N/A'

    # Adding new fields based on provided CSS Selectors
    market_cap = clean_text(soup.select_one('div.compess:nth-child(1) > p > span.Number').get_text()) if soup.select_one('div.compess:nth-child(1) > p > span.Number') else 'N/A'
    enterprise_value = clean_text(soup.select_one('div.compess:nth-child(2) > p > span.Number').get_text()) if soup.select_one('div.compess:nth-child(2) > p > span.Number') else 'N/A'
    no_of_shares = clean_text(soup.select_one('div.compess:nth-child(3) > p > span.Number').get_text()) if soup.select_one('div.compess:nth-child(3) > p > span.Number') else 'N/A'
    pb_ratio = clean_text(soup.select_one('div.compess:nth-child(5) > p').get_text()) if soup.select_one('div.compess:nth-child(5) > p') else 'N/A'
    face_value = clean_text(soup.select_one('div.compess:nth-child(6) > p').get_text()) if soup.select_one('div.compess:nth-child(6) > p') else 'N/A'
    div_yield = clean_text(soup.select_one('div.compess:nth-child(7) > p').get_text()) if soup.select_one('div.compess:nth-child(7) > p') else 'N/A'
    book_value = clean_text(soup.select_one('div.compess:nth-child(8) > p > span.Number').get_text()) if soup.select_one('div.compess:nth-child(8) > p > span.Number') else 'N/A'

    # Extract CASH and DEBT, and clean up values
    cash = clean_text(soup.find('span', {'id': 'mainContent_ltrlCash'}).get_text(), retain_cr=True) if soup.find('span', {'id': 'mainContent_ltrlCash'}) else 'N/A'
    debt = clean_text(soup.find('span', {'id': 'mainContent_ltrlDebt'}).get_text(), retain_cr=True) if soup.find('span', {'id': 'mainContent_ltrlDebt'}) else 'N/A'

    promoter_holding = clean_text(soup.select_one('div.compess:nth-child(11) > p').get_text()) if soup.select_one('div.compess:nth-child(11) > p') else 'N/A'
    eps_ttm = clean_text(soup.select_one('div.compess:nth-child(12) > p > span.Number').get_text()) if soup.select_one('div.compess:nth-child(12) > p > span.Number') else 'N/A'
    sales_growth = clean_text(soup.select_one('div.compess:nth-child(13) > p > span.Number').get_text()) if soup.select_one('div.compess:nth-child(13) > p > span.Number') else 'N/A'

    return {
        'Company Name': company_name,
        'Sector': sector,
        'LTP': ltp,
        'P/E Ratio': pe_ratio,  # Updated P/E Ratio
        'Market Cap': market_cap,
        'Enterprise Value': enterprise_value,
        'No. of Shares': no_of_shares,
        'P/B Ratio': pb_ratio,
        'Face Value': face_value,
        'Div. Yield': div_yield,
        'Book Value (TTM)': book_value,
        'CASH': cash,
        'DEBT': debt,
        'Promoter Holding': promoter_holding,
        'EPS (TTM)': eps_ttm,
        'Sales Growth': sales_growth,
    }

# Read URLs from the file and scrape data
def scrape_urls(url_file):
    with open(url_file, 'r') as file:
        urls = [url.strip() for url in file.readlines()]

    results = []
    
    # Use tqdm to create a progress bar for the loop
    for url in tqdm(urls, desc="Scraping URLs", unit="url", ncols=100):
        if not url:
            continue  # Skip empty URLs
        
        # Fetch the page content using random user-agent
        html_content = fetch_page(url)
        
        if html_content is None:
            results.append([url] + ['No data found'] * 16)  # Skip further extraction if fetch fails
            continue
        
        # Extract data from the page
        data = extract_data(html_content)
        
        # Append the data to results
        results.append([url] + [data[key] for key in data])
    
    return results

# Write the results to a CSV file
def save_results(results, output_file="scraped_results.csv"):
    # Define the CSV column headers
    headers = ['URL', 'Company Name', 'Sector', 'LTP', 'P/E Ratio', 'Market Cap (Cr)', 'Enterprise Value (Cr)', 'No. of Shares (Cr)', 'P/B Ratio', 'Face Value', 'Div. Yield', 'Book Value (TTM)', 'CASH', 'DEBT', 'Promoter Holding', 'EPS (TTM)', 'Sales Growth (%)']

    # Open the CSV file for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(headers)
        
        # Write the rows of data
        writer.writerows(results)

# Main function to run the scraper
if __name__ == "__main__":
    url_file = 'urls.txt'  # File containing list of URLs to scrape
    results = scrape_urls(url_file)
    save_results(results)
    print("Scraping complete. Results saved in 'scraped_results.csv'.")
