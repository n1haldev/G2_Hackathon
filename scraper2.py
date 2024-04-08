import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

# Function to extract data from a webpage
def extract_data(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data from various HTML tags
        extracted_data = {}
        for tag_name in ['h1', 'h2', 'p', 'h3', 'h4', 'h5', 'h6']:
            tags = soup.find_all(tag_name)
            tag_data = []
            for tag in tags:
                tag_text = tag.get_text(strip=True)
                tag_data.append(tag_text)
            extracted_data[tag_name] = tag_data

        return extracted_data
    else:
        print(f"Failed to retrieve data from {url}")

# Function to extract URLs from a webpage
def extract_urls(url, company_domain):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <a> tags containing URLs
        links = soup.find_all('a', href=True)

        # Extract and normalize URLs
        extracted_urls = set()  # Use a set to store unique URLs
        for link in links:
            href = link['href']
            # Normalize relative URLs
            absolute_url = urljoin(url, href)
            # Filter out non-http(s) URLs and external links
            parsed_url = urlparse(absolute_url)
            if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc == company_domain:
                extracted_urls.add(absolute_url)  # Add URL to the set

        return extracted_urls
    else:
        print(f"Failed to retrieve data from {url}")

def main():
    url = 'https://aim-agency.com/'   # input url
    company_domain = 'aim-agency.com'


    # Extract internal URLs from the main page
    internal_urls = extract_urls(url, company_domain)
    print("Internal URLs found on the page:")
    for internal_url in internal_urls:
        print(internal_url)
        # Extract data from each internal URL
        data = extract_data(internal_url)
        if data:
            print("Data from the internal page:")
            for tag_name, data_list in data.items():
                print(f"Data from <{tag_name}> tags:")
                for data_item in data_list:
                    print(data_item)
                print()

if __name__ == "__main__":
    main()
