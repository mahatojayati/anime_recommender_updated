import streamlit as st
import pandas as pd
import requests
from recommender_core import get_recommendations  # your existing logic

# Load dataset
df = pd.read_csv('anime.csv')

st.set_page_config(page_title="Anime Recommendation System", layout="centered")
st.title("Anime Recommendation System")
st.write("Select an anime you like and get recommendations with live summaries (via MyAnimeList).")

# Function to fetch summary from Jikan API
def fetch_summary(anime_title):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={anime_title}&limit=1"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                return data["data"][0].get("synopsis", "Summary not available.")
        return "Summary not available."
    except:
        return "Summary not available."

# Dropdown
anime_list = df['name'].dropna().unique()
selected_anime = st.selectbox("Choose an Anime", sorted(anime_list))

if st.button("Recommend"):
    with st.spinner("Fetching recommendations..."):
        recommendations = get_recommendations(selected_anime)

    st.subheader("Recommended Animes with Summaries:")
    for anime in recommendations:
        st.markdown(f"### {anime}")
        summary = fetch_summary(anime)
        st.write(summary)
