from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def calculate_match_score(cv_text: str, job_description: str) -> float:
    if not cv_text or not job_description:
        return 0.0

    # Extract skills/keywords (single words and 2-3 word phrases)
    def extract_keywords(text):
        text = text.lower()
        # Split by common delimiters
        tokens = re.split(r'[,\n•\-•\t]+', text)
        keywords = []
        for token in tokens:
            token = token.strip()
            if token and len(token) > 2:
                keywords.append(token)
        return " ".join(keywords)

    cv_keywords = extract_keywords(cv_text)
    job_keywords = extract_keywords(job_description)

    if not cv_keywords or not job_keywords:
        return 0.0

    # Use TF-IDF on extracted keywords
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform([cv_keywords, job_keywords])
    except ValueError:
        return 0.0

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    score = float(similarity[0][0] * 100)
    return round(score, 1)