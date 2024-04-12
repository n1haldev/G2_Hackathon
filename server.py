from flask import Flask, request, jsonify
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
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL not provided in request body.'}), 400

    company_domain = scraper.extract_domain_name(url)
    internal_urls = scraper.extract_urls(url, company_domain)
    text_data = ""
    if internal_urls:
        for internal_url in internal_urls:
                data = scraper.extract_data(internal_url)
                if data:
                    for tag_name, data_list in data.items():
                        for data_item in data_list:
                            text_data += data_item + "\n"
        
        summarized_text = summarizer.summarize_text(text_data, url)
        
        # Print the summarized text to the terminal
        print("Summarized Text:")
        print(summarized_text.text)
        
        return jsonify({'Summarized Text': summarized_text.text}), 200
    else:
        data = scraper.extract_data(url)
        if data:
            for _, data_list in data.items():
                for data_item in data_list:
                    text_data += data_item + "\n"
        
        summarized_text = summarizer.summarize_text(text_data, url)
        print(summarized_text.text)
        return jsonify({'Summarized Text': summarized_text.text}), 200

if __name__ == '__main__':
    app.run(debug=True)
