import streamlit as st
import pandas as pd
import requests
from recommendation import recommend_anime  # Your existing function

# Load dataset (still needed for anime list & selection)
df = pd.read_csv('anime.csv')

st.set_page_config(page_title="Anime Recommendation System", layout="centered")
st.title("Anime Recommendation System")
st.write("Select an anime you like and get recommendations with real-time summaries.")

# Function to fetch summary from Jikan API
def fetch_summary(anime_title):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={anime_title}&limit=1"
        response = requests.get(url)
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            return data["data"][0]["synopsis"]
        else:
            return "Summary not available."
    except Exception as e:
        return f"Error fetching summary: {e}"

# Dropdown for anime selection
anime_list = df['name'].dropna().unique()
selected_anime = st.selectbox("Choose an Anime", sorted(anime_list))

if st.button("Recommend"):
    with st.spinner("Fetching recommendations..."):
        recommendations = recommend_anime(selected_anime)

    st.subheader("Recommended Animes:")
    for anime in recommendations:
        st.markdown(f"### {anime}")
        summary = fetch_summary(anime)
        st.write(summary)
