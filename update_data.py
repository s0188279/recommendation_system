import sqlite3
import pandas as pd


def update_movies():
    conn = sqlite3.connect('october.db')

    new_movies = pd.read_csv('movies.csv', sep=';', encoding='utf-8-sig')
    new_movies.to_sql('movies', conn, if_exists='replace', index=False)

    ratings_orig = pd.read_csv('ratings.csv')
    valid_ids = new_movies['movieId'].unique()
    filtered_ratings = ratings_orig[ratings_orig['movieId'].isin(valid_ids)]

    filtered_ratings.to_sql('ratings', conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()
    print(f"База обновлена! Теперь в ней {len(new_movies)} фильмов.")


if __name__ == "__main__":
    update_movies()
