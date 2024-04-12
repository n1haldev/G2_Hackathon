from summa import keywords

class KeywordExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_keywords(self, text, num_of_keywords=10):
        keywords_with_scores = keywords.keywords(text, scores=True)
        return keywords_with_scores[:num_of_keywords]