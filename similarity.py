import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# создание TF-IDF матрицы
def build_similarity_matrix(df):
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(df["content_text"])
    return matrix

# рекомендации
def get_recommendations(title, df, matrix, n=10):
    # переводим в нижний регистр
    title = title.lower().strip()
    # ищем фильм
    movie_index = None
    for index, row in df.iterrows():
        if row["title_normalized"] == title:
            movie_index = index
            break

    # если фильм не найден
    if movie_index is None:
        print("Movie not found")
        return pd.DataFrame()
    # считаем похожесть
    cosine_scores = linear_kernel(
        matrix[movie_index],
        matrix
    ).flatten()
    # сортируем
    similar_indices = cosine_scores.argsort()[::-1]
    rows = []
    for idx in similar_indices:
        # пропускаем сам фильм
        if idx == movie_index:
            continue
        row = df.iloc[idx]

        rows.append({
            "title": row["title"],
            "type": row["type"],
            "release_year": row["release_year"],
            "score": cosine_scores[idx]
        })
        if len(rows) >= n:
            break

    return pd.DataFrame(rows)