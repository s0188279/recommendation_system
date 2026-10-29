import sqlite3
import pandas as pd
import os


def init_database():
    db_name = 'october.db'
    movies_file = 'movies.csv'
    ratings_file = 'ratings.csv'

    if not os.path.exists(movies_file):
        print(f"Ошибка: Файл {movies_file} не найден!")
        return
    if not os.path.exists(ratings_file):
        print(f"Ошибка: Файл {ratings_file} не найден! (Нужен оригинал с оценками)")
        return

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    print("Создаем таблицы...")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            userId INTEGER,
            movieId INTEGER,
            rating REAL,
            timestamp INTEGER,
            PRIMARY KEY (userId, movieId)
        )
    ''')

    try:
        print("Загружаем фильмы...")
        movies_df = pd.read_csv(movies_file, sep=';', encoding='utf-8-sig')
        movies_df.to_sql('movies', conn, if_exists='replace', index=False)

        print("Загружаем и фильтруем оценки (это может занять секунд 10)...")
        ratings_df = pd.read_csv(ratings_file)

        valid_ids = movies_df['movieId'].unique()
        filtered_ratings = ratings_df[ratings_df['movieId'].isin(valid_ids)]

        filtered_ratings.to_sql('ratings', conn, if_exists='replace', index=False)

        conn.commit()
        print(f"Успех! База данных '{db_name}' готова.")
        print(f"Загружено фильмов: {len(movies_df)}")
        print(f"Загружено оценок: {len(filtered_ratings)}")

    except Exception as e:
        print(f"Произошла ошибка при обработке данных: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    init_database()
