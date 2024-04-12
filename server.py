from flask import Flask, request, jsonify, render_template

from WebScraper import WebScraper
from Summarizer import Summarizer
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

goog_api_key = os.getenv("GOOG_API_KEY")

if not goog_api_key:
    raise ValueError("Google Api not found!")

app = Flask(__name__)

# Initialize WebScraper and Summarizer instances
scraper = WebScraper(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'})
genai.configure(api_key=goog_api_key)
model = genai.GenerativeModel('gemini-pro')
summarizer = Summarizer(model=model)

@app.route('/', methods=['POST'])
def scrape_preprocess_and_summarize():
    # Get URL from request body
    request_data = request.get_json()
    url = request_data.get('url')
    if not url:
        return jsonify({'error': 'URL not provided in request body.'}), 400

    # Scrape data from the URL
    # company_domain = scraper.extract_domain_name(url)
    # internal_urls = scraper.extract_urls(url, company_domain)
    # text_data = ""
    # if internal_urls:
    #     for internal_url in internal_urls:
    #         data = scraper.extract_data(internal_url)
    #         # Preprocess text
    #         if data:
    #             # text_data = '\n'.join(d for d in data.values())
    #             for text in data.values():
    #                 # text_data += text
    #                 print(text)
    #                 for inner_text in text:
    #                     print(inner_text)
    #                     text_data += inner_text
    #             # Extract 20 keywords
    #             # keywords = text_preprocessor.extract_keywords(num_keywords=20)
    #             summarized_text = summarizer.summarize_text(text_data, url)
    #             # Return summarized text in JSON format
    #             return jsonify({'summarized_text': summarized_text})
    # else:
    #     return jsonify({'error': 'No internal URLs found on the page.'}), 404

    # url = 'https://aim-agency.com/'   # input url

    # Extract internal URLs from the main page
    company_domain = scraper.extract_domain_name(url)
    internal_urls = scraper.extract_urls(url, company_domain)
    text_data = ""
    if internal_urls:
        for internal_url in internal_urls:
                # Extract data from each internal URL
                data = scraper.extract_data(internal_url)
                if data:
                    for tag_name, data_list in data.items():
                        # file.write(f"Data from <{tag_name}> tags:\n")
                        for data_item in data_list:
                            print(data_item + "\n")
                            text_data += data_item + "\n"
        
        summarized_text = summarizer.summarize_text(text_data, url)
        print(summarized_text.text)
        return jsonify({'Summarized Text': summarized_text.text}), 200

    else:
        data = scraper.extract_data(url)
        if data:
            for _, data_list in data.items():
                # file.write(f"Data from <{tag_name}> tags:\n")
                for data_item in data_list:
                    print(data_item + "\n")
                    text_data += data_item + "\n"
                    # file.write(data_item + '\n')
                # file.write('\n')
        # return jsonify({'error': 'No internal URLs found on the page.'}), 404
        summarized_text = summarizer.summarize_text(text_data, url)
        print(summarized_text.text)
        return jsonify({'Summarized Text': summarized_text.text}), 200


if __name__ == '__main__':
    app.run(debug=True)
