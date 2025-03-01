import pandas as pd
import streamlit as st
import pickle
import requests

movies_dict = pickle.load(open('movies_dict_hindi.pkl', 'rb'))
similarity = pickle.load(open('similarity_hindi.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
st.title('Movie Recommender System')

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyZjJhYWZjYjU4ODA5ZTdkZWU0ZTk2Yjg5ZDRjZTFlMCIsIm5iZiI6MTczNDM3MzgyNC4wMjEsInN1YiI6IjY3NjA3MWMwNjczZmZlYTBmMjdkZjAzYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Jp-y2fZP1EMNTXrm5KlBnPUf4LpYjAn0sY4lOo62ih0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if 'poster_path' in data and data['poster_path']:
            return "http://image.tmdb.org/t/p/w500" + data['poster_path']
        return None
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_list = []
    recommended_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_list.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        recommended_poster.append(poster if poster else "placeholder_image_url")
    return recommended_list, recommended_poster


selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values
)
st.write("You selected:", selected_movie_name)

if st.button("Recommend"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    for col, name, poster in zip([col1, col2, col3, col4, col5],
                                 recommended_movie_names,
                                 recommended_movie_posters):
        with col:

            if poster:
                st.image(poster)
            else:
                st.write("No poster available")
            st.text(name)