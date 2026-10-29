import streamlit as st
import sqlite3
import pandas as pd
from api_utils import get_movie_info
from recommender import get_recommendations

st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important; 
        padding-bottom: 0rem !important;
        max-width: 95% !important; 
    }

    .main-title {
        margin-top: -30px !important; 
        margin-bottom: 10px !important;
        padding: 0 !important;
        font-size: 3rem !important;
        text-align: center;
        color: #f57c00;
    }
    /* ВКЛАДКИ (Вход/Регистрация) */
    button[data-baseweb="tab"] {
        font-size: 18px !important;
        color: #8b949e !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #f57c00 !important;
        border-bottom-color: #f57c00 !important;
    }
    .stTextInput input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus {
        border-color: #f57c00 !important;
    }

    .stTextInput div[data-baseweb="input"] {
        background-color: #161b22 !important;
        border-radius: 10px !important;
        border: 1px solid #30363d !important;
        height: 50px !important;
    }

    .stTextInput div[data-baseweb="input"] button {
        height: 30px !important;
        width: 30px !important;
        margin-right: 10px !important;
        background: transparent !important;
        border: none !important;
    }

    [data-testid="stDialog"] button {
        margin-top: 10px;
        height: 45px;
        font-weight: bold !important;
    }

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="css"], .stMarkdown {
        font-family: 'Inter', sans-serif !important;
        font-size: 18px !important; 
    }

    .nav-link {
        display: block;
        padding: 10px 15px;
        color: #f57c00 !important;
        text-decoration: none !important;
        font-weight: bold;
        font-size: 20px !important;
        border-radius: 8px;
        transition: 0.3s;
    }
    .nav-link:hover {
        background: rgba(245, 124, 0, 0.1);
        transform: translateX(5px);
    }

    h1, h2 {
        font-size: 2.5rem !important;
        margin-top: 2rem !important;
    }

    :root {
        --primary-color: #f57c00 !important;
        --base: dark !important;
    }

    .stApp { background-color: #0d1117; }

    button, [data-testid="baseButton-secondary"], [data-testid="baseButton-primary"] {
        height: 50px !important;
        border-radius: 12px !important; 
        font-size: 16px !important;
        font-weight: 600 !important;
        background-color: #21262d !important;
        color: #f57c00 !important;
        border: 1px solid #30363d !important;
        width: 100% !important;
        transition: 0.3s !important;
    }

    button:hover {
        background-color: #f57c00 !important;
        color: white !important;
        border-color: #f57c00 !important;
    }

    button[aria-label="Close"] {
        width: 40px !important;
        height: 40px !important;
        background: #161b22 !important;
        border-radius: 50% !important;
        top: 10px !important;
        right: 10px !important;
    }

    button:focus, button:active, button:focus-visible, 
    [data-testid="baseButton-secondary"]:focus, 
    [data-testid="baseButton-secondary"]:active {
        background-color: #21262d !important; 
        color: #f57c00 !important;
        border-color: #f57c00 !important;
        box-shadow: none !important;
        outline: none !important;
    }

    .stButton > button:focus {
        background-color: #21262d !important;
        color: #f57c00 !important;
    }

    [data-testid="stImage"] img {
        height: 400px !important;
        object-fit: cover !important;
        border-radius: 12px !important;
        border: 1px solid #30363d !important;
    }

    .stMarkdown div p strong {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        height: 2.8em;
        line-height: 1.4;
        color: #c9d1d9 !important;
        margin-top: 5px;
    }

    .nav-link {
        color: #f57c00 !important;
        text-decoration: none !important;
        font-weight: bold;
    }

    [data-testid="stStatusWidget"] { display: none; }
    
    div[data-testid="stDialog"] div[role="dialog"] {
        width: 80vw !important;
        max-width: 950px !important;
        min-width: 300px !important;
        margin: 0 auto !important;
    }

    div[data-testid="stDialog"] .stColumn {
        width: 100% !important;
    }
 
    .user-welcome {
        font-size: 24px !important;
        font-weight: bold !important;
        color: white !important;
    }

    button p {
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    .profile-movie-title {
        font-size: 22px !important;
        font-weight: bold !important;
        padding-top: 10px;
    }
    .profile-movie-rating {
        font-size: 26px !important;
        color: #f57c00 !important;
        font-weight: 800 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align: center; color: #f57c00;">🍿 Кинотеатр "Октябрь"</h1>', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def cached_get_movie_info(title):
    return get_movie_info(title)

st.set_page_config(page_title="Октябрь", layout="wide")

def get_db():
    return sqlite3.connect('october.db')

if 'user' not in st.session_state:
    st.session_state.user = None

@st.dialog("Вход / Регистрация")
def auth_dialog():
    t1, t2 = st.tabs(["Вход", "Регистрация"])
    with t1:
        l = st.text_input("Логин")
        p = st.text_input("Пароль", type="password")
        if st.button("Войти", use_container_width=True):
            with get_db() as conn:
                u = conn.execute("SELECT * FROM users WHERE login=? AND password=?", (l, p)).fetchone()
                if u:
                    st.session_state.user = {"id": u[0], "login": u[1]}
                    st.rerun()
                else:
                    st.error("Ошибка входа")
    with t2:
        rl = st.text_input("Новый логин")
        rp = st.text_input("Новый пароль", type="password")
        if st.button("Создать", use_container_width=True):
            with get_db() as conn:
                try:
                    conn.execute("INSERT INTO users (login, password) VALUES (?,?)", (rl, rp))
                    conn.commit()
                    st.success("Аккаунт создан!")
                except:
                    st.error("Логин занят")

if 'show_auth' not in st.session_state:
    st.session_state.show_auth = False

@st.dialog("Подробнее")
def details(m_id, title, genres):
    info = cached_get_movie_info(title)
    c1, c2 = st.columns([1, 2])

    with c1:
        poster_url = info.get('poster')
        if not poster_url or poster_url == "N/A":
            poster_url = "https://via.placeholder.com/400x600/161b22/f57c00?text=No+Poster"
        st.image(poster_url, use_container_width=True)

    with c2:
        st.subheader(title)
        st.caption(genres)
        st.write(info['desc'])

        st.divider()
        val = st.slider("Ваша оценка", 1.0, 10.0, 5.0, step=0.5, key=f"rev_{m_id}")

        if st.button("Оценить", use_container_width=True):
            if st.session_state.user:
                with get_db() as conn:
                    conn.execute(
                        "INSERT OR REPLACE INTO ratings (userId, movieId, rating) VALUES (?,?,?)",
                        (st.session_state.user['id'], m_id, val)
                    )
                    conn.commit()
                st.success(f"Вы поставили {val}!")
            else:
                st.session_state.show_auth = True
                st.rerun()


@st.dialog("Личный кабинет", width="large")
def profile_dialog():
    st.write(f"### Ваши оценки, {st.session_state.user['login']}")

    with get_db() as conn:
        query = """
            SELECT m.title, r.rating 
            FROM ratings r
            JOIN movies m ON r.movieId = m.movieId
            WHERE r.userId = ?
        """
        user_ratings = pd.read_sql(query, conn, params=(st.session_state.user['id'],))

    if user_ratings.empty:
        st.info("Вы еще не оценивали фильмы.")
    else:
        for _, row in user_ratings.iterrows():
            col_img, col_txt = st.columns([1, 2])
            movie_info = get_movie_info(row['title'])
            with col_img:
                st.image(movie_info['poster'], width=400)
            with col_txt:
                st.markdown(f'<p class="profile-movie-title">{row['title']}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="profile-movie-rating">⭐ {row["rating"]}</p>', unsafe_allow_html=True)
            st.divider()


def render_carousel(genre_name, movies_list):
    st.markdown(f'<div id="{genre_name.lower()}"></div>', unsafe_allow_html=True)
    st.header(f"🍿 {genre_name}")

    state_key = f"pos_{genre_name}"
    if state_key not in st.session_state:
        st.session_state[state_key] = 0

    cols = st.columns([0.5, 2, 2, 2, 2, 2, 0.5], vertical_alignment="center")

    current_pos = st.session_state[state_key]

    with cols[0]:
        if st.button("⬅", key=f"prev_{genre_name}"):
            if current_pos > 0:
                st.session_state[state_key] -= 5
                st.rerun()

    visible_movies = movies_list[current_pos: current_pos + 5]

    for i, movie in enumerate(visible_movies):
        with cols[i + 1]:
            info = cached_get_movie_info(movie['title'])
            poster_url = info.get('poster')

            if not poster_url or poster_url == "N/A" or len(poster_url) < 10:
                clean_title = movie['title'].replace(" ", "+")
                poster_url = f"https://via.placeholder.com/400x600/161b22/f57c00?text={clean_title}"

            st.image(poster_url, use_container_width=True)
            st.write(f"**{movie['title']}**")
            if st.button("Подробнее", key=f"btn_{genre_name}_{movie['movieId']}", width='stretch'):
                details(movie['movieId'], movie['title'], movie['genres'])

    with cols[6]:
        if st.button("➡", key=f"next_{genre_name}"):
            if current_pos + 5 < len(movies_list):
                st.session_state[state_key] += 5
                st.rerun()

with st.sidebar:
    if st.session_state.user:

        st.markdown(f'<p class="user-welcome">👤 {st.session_state.user["login"]} </p>',
                    unsafe_allow_html=True)
        if st.button("🗄️ Личный кабинет", width='stretch'):
            profile_dialog()
        if st.button("🚪 Выйти", width='stretch'):
            st.session_state.user = None
            st.rerun()
    else:
        if st.button("🔑 Войти", width='stretch'):
            auth_dialog()

    st.divider()
    st.write("### Навигация")
    for g in ["Боевик", "Комедия", "Драма", "Ужасы", "Мультфильм"]:
        st.markdown(f'<a href="#{g.lower()}" class="nav-link">{g}</a>', unsafe_allow_html=True)

if st.session_state.user:
    recs = get_recommendations(st.session_state.user['id'])
    if recs:
        render_carousel("Специально для вас", recs)
    else:
        st.info("Поставьте больше оценок!")

st.divider()

with get_db() as conn:
    movies_df = pd.read_sql("SELECT * FROM movies", conn)

genres = ["Боевик", "Комедия", "Драма", "Ужасы", "Мультфильм"]

for genre in genres:

    genre_movies = movies_df[movies_df['genres'].str.contains(genre, na=False)].to_dict('records')

    if genre_movies:
        render_carousel(genre, genre_movies)
    st.divider()

if st.session_state.show_auth:
    st.session_state.show_auth = False 
    auth_dialog()
