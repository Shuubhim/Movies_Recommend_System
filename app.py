import pickle
import streamlit as st
import requests
import pandas as pd

# OMDb API Key
OMDB_API_KEY = "48d7a0c5"

def fetch_poster_omdb(movie_name):
    """
    Fetches the poster URL for a given movie using the OMDb API.
    If the poster is not available, returns a placeholder image.
    """
    try:
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data.get('Poster', "https://via.placeholder.com/500x750?text=No+Image+Available")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching movie poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    """
    Recommends 5 similar movies based on the given movie name.
    Fetches posters for each recommended movie using OMDb API.
    """
    movies_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies_list = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommend_movies_poster.append(fetch_poster_omdb(movie_title))  # Fetch poster
        recommend_movies_list.append(movie_title)
    return recommend_movies_list, recommend_movies_poster

# Load precomputed data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movies Recommender System')

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)  # Updated to use st.columns
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
