from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def text_similarity(text_a: str, text_b: str) -> float:
  """Return how similar two texts are, as a score from 0 to 100.

  Uses TF-IDF vectors + cosine similarity, so it catches meaning that
  pure keyword matching misses (e.g. "database knowledge" vs "SQL").
  """
  a = (text_a or "").strip()
  b = (text_b or "").strip()

  # Empty input cannot be vectorized - just say "no overlap".
  if not a or not b:
    return 0.0

  # Build a vocabulary from BOTH texts, then weight each one.
  # lowercase=True so "SQL" and "sql" count as the same word.
  vectorizer = TfidfVectorizer(lowercase=True)
  try:
    matrix = vectorizer.fit_transform([a, b])
  except ValueError:
    # e.g. texts made only of 1-char tokens -> empty vocabulary.
    return 0.0

  # matrix[0] = resume vector, matrix[1] = job vector.
  # cosine_similarity returns [[1.0]] for identical texts.
  score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
  return round(float(score) * 100, 1)