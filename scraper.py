from bs4 import BeautifulSoup
import requests

url = input().strip()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    h1 = soup.find_all('h1')
    h2 = soup.find_all('h2')
    h3 = soup.find_all('h3')
    keyword_tags = h1 + h2 + h3
    description_tags = soup.find_all('p')

    keywords = [keyword_tag.text for keyword_tag in keyword_tags]
    descriptions = [description_tag.text for description_tag in description_tags]

    company_name = url.split('.')[1]

    with open(company_name+"_keywords.txt", 'w') as keywords_file:
        for keyword in keywords:
            keywords_file.write(keyword + "\n")

    with open(company_name+"_descriptions.txt", 'w') as descriptions_file:
        for description in descriptions:
            descriptions_file.write(description + "\n")

    # print(keywords)
    # print(descriptions)

else:
    print("Unable to reach the url! Please check if url is correct and accessible!")