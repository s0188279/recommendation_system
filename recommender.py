import pandas as pd
import sqlite3
from scipy.sparse.linalg import svds
import numpy as np


def get_recommendations(user_id, db_path='october.db'):
    with sqlite3.connect(db_path) as conn:
        all_ratings = pd.read_sql("SELECT userId, movieId, rating FROM ratings", conn)
        movies = pd.read_sql("SELECT movieId, title, genres FROM movies", conn)

    if all_ratings[all_ratings['userId'] == user_id].empty:
        return []

    try:
        all_ratings = all_ratings.drop_duplicates(subset=['userId', 'movieId'], keep='last')

        user_movie_matrix = all_ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)

        matrix = user_movie_matrix.values
        user_ratings_mean = np.mean(matrix, axis=1)
        matrix_demeaned = matrix - user_ratings_mean.reshape(-1, 1)

        U, sigma, Vt = svds(matrix_demeaned, k=min(10, matrix.shape[1] - 1))
        sigma = np.diag(sigma)

        all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

        user_idx = user_movie_matrix.index.get_loc(user_id)

        preds_df = pd.DataFrame(all_user_predicted_ratings[user_idx],
                                index=user_movie_matrix.columns, columns=['prediction'])

        already_rated = all_ratings[all_ratings['userId'] == user_id]['movieId']
        recommendations = preds_df[~preds_df.index.isin(already_rated)]

        top_ids = recommendations.sort_values('prediction', ascending=False).head(15).index

        return movies[movies['movieId'].isin(top_ids)].to_dict('records')

    except Exception as e:
        print(f"Ошибка в расчетах: {e}")
        return []
