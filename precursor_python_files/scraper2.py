import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

# Function to extract data only from the main tag of a webpage
def extract_data(url):
    with requests.Session() as session:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract data only from the main tag
            main_tag = soup.find('main')
            if main_tag:
                extracted_data = {}
                for tag_name in ['p', 'span']:
                    tags = main_tag.find_all(tag_name)
                    tag_data = []
                    for tag in tags:
                        tag_text = tag.get_text(strip=True)
                        tag_data.append(tag_text)
                    extracted_data[tag_name] = tag_data

                return extracted_data
            else:
                print("Main tag not found on the page.")
                return None
        else:
            print(f"Failed to retrieve data from {url}")
            return None

# Function to extract URLs from a webpage
def extract_urls(url, company_domain):
    with requests.Session() as session:
        response = session.get(url, allow_redirects=True)
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

# Function to extract domain name from a URL
def extract_domain_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain

def main():
    url = 'https://aim-agency.com/'   # input url
    company_domain = extract_domain_name(url)

    output_file = 'scrapedData.txt'
    with open(output_file, 'w', encoding='utf-8') as file:
        # Extract internal URLs from the main page
        internal_urls = extract_urls(url, company_domain)
        if internal_urls:
            for internal_url in internal_urls:
                # Extract data from each internal URL
                data = extract_data(internal_url)
                if data:
                    for tag_name, data_list in data.items():
                        # file.write(f"Data from <{tag_name}> tags:\n")
                        for data_item in data_list:
                            file.write(data_item + '\n')
                        file.write('\n')
        else:
            print("No internal URLs found on the page. Extracting data directly from the main URL.")
            # Extract data from the main URL
            data = extract_data(url)
            if data:
                for tag_name, data_list in data.items():
                    # file.write(f"Data from <{tag_name}> tags:\n")
                    for data_item in data_list:
                        file.write(data_item + '\n')
                    file.write('\n')
            else:
                print("No data found on the main page.")

if __name__ == "__main__":
    main()
