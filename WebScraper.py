import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class WebScraper:
    def __init__(self, headers):
        self.headers = headers

    def extract_data(self, url):
        with requests.Session() as session:
            response = session.get(url, headers=self.headers)
            if response.status_code == 200 or response.status_code == 201:
                soup = BeautifulSoup(response.content, 'html.parser')

                # # Extract data only from the main tag
                # main_tag = soup.find('main')
                # if main_tag:
                extracted_data = {}
                for tag_name in ['p', 'span']:
                    tags = soup.find_all(tag_name)
                    tag_data = []
                    for tag in tags:
                        tag_text = tag.get_text(strip=True)
                        tag_data.append(tag_text)
                    extracted_data[tag_name] = tag_data
                # print(extracted_data)
                return extracted_data
                # else:
                #     print("Main tag not found on the page.")
                #     return None
            else:
                print(f"Failed to retrieve data from {url}")
                return None

    def extract_urls(self, url, company_domain):
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

    def extract_domain_name(self, url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return domain