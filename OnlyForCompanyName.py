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
    response = requests.get(url, headers=headers)
    return response.text

# Function to extract the required information from the page
def extract_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting data based on HTML structure of the page
    company_name = soup.find('span', {'id': 'mainContent_ltrlCompName'}).get_text(strip=True) if soup.find('span', {'id': 'mainContent_ltrlCompName'}) else 'N/A'
    sector = soup.find('a', {'class': 'font-weight-bold'}).get_text(strip=True) if soup.find('a', {'class': 'font-weight-bold'}) else 'N/A'
    ltp = soup.find('span', {'class': 'Number'}).get_text(strip=True) if soup.find('span', {'class': 'Number'}) else 'N/A'

    # You can add more fields based on the structure of the web pages you're scraping

    return {
        'Company Name': company_name,
        'Sector': sector,
        'LTP': ltp,
        # Add more fields as needed
    }

# Read URLs from the file and scrape data
def scrape_urls(url_file):
    with open(url_file, 'r') as file:
        urls = file.readlines()

    results = []
    
    # Use tqdm to create a progress bar for the loop
    for url in tqdm(urls, desc="Scraping URLs", unit="url", ncols=100):
        url = url.strip()  # Remove any extra spaces or newline characters
        
        # Fetch the page content using random user-agent
        html_content = fetch_page(url)
        
        # Extract data from the page
        data = extract_data(html_content)
        
        # Append the data to results
        if data:
            results.append([url, data['Company Name'], data['Sector'], data['LTP']])
        else:
            results.append([url, 'No data found', 'No data found', 'No data found'])

    return results

# Write the results to a CSV file
def save_results(results, output_file="scraped_results.csv"):
    # Define the CSV column headers
    headers = ['URL', 'Company Name', 'Sector', 'LTP']

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
