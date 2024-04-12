!pip install summa
from summa import keywords

file_path = 'scrapedData.txt'  # Enter file name
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read() 

TR_keywords = keywords.keywords(text, scores=True)
print(TR_keywords[0:100])  # adjust the number of keywords here