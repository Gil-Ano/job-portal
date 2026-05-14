from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_score(cv_text: str, job_description: str) -> float:
    """
    Compare CV text with job description and return a match percentage (0-100).
    Uses TF-IDF vectorization and cosine similarity.
    """
    if not cv_text or not job_description:
        return 0.0

    # Create TF-IDF vectors from the two texts
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform([cv_text, job_description])
    except ValueError:
        return 0.0

    # Calculate cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    # Convert to percentage
    score = float(similarity[0][0] * 100)
    return round(score, 1)