import requests
import streamlit as st

API_KEY = ""

@st.cache_data(ttl=3600)
def get_movie_info(title):
    try:
        headers = {"X-API-KEY": API_KEY}
        url = f"https://api.kinopoisk.dev/v1.4/movie/search?query={title}"
        res = requests.get(url, headers=headers, timeout=5).json()
        if res.get('docs'):
            m = res['docs'][0]
            poster = m.get('poster', {}).get('url') or "https://via.placeholder.com/300x450/161b22/f57c00?text=ОКТЯБРЬ"
            return {"poster": poster, "desc": m.get('description'), "rating": m.get('rating', {}).get('kp')}
    except: pass
    return {"poster": "https://via.placeholder.com/300x450/161b22/f57c00?text=ОКТЯБРЬ", "desc": "", "rating": 0}
