#!pip install transformers
from transformers import pipeline

# var which should have keyword/summary
ARTICLE = """
#INPUT TEXT TO SUMMARISER

"""

# Check if ARTICLE is empty or content is not loaded
if not ARTICLE.strip():
    print("Error: ARTICLE is empty or content not loaded.")
    exit()

# Initialize the summarization pipeline
try:
    summarizer = pipeline("summarization")
except Exception as e:
    print("Error initializing summarization pipeline:", e)
    exit()

# Split the ARTICLE into smaller chunks
# 2048 to avoid exceeding the max token limit
chunks = [ARTICLE[i:i + 2048] for i in range(0, len(ARTICLE), 2048)]

# Summarize each chunk
for chunk in chunks:
    try:
        summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
    except Exception as e:
        print("Error summarizing chunk:", e)
        continue
    
    # Check if summary is generated
    if not summary:
        print("Error: Summary not generated for chunk.")
        continue
    
    print(summary)

# Saving the summaries into another file
try:
    with open("summaries.txt", "w") as file:
        for s in summary:
            file.write(s['summary_text'] + "\n")
    print("Summaries saved to 'summaries.txt'.")
except Exception as e:
    print("Error saving summaries to file:", e)
