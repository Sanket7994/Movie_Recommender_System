import streamlit as st
import pickle
import pandas as pd
import requests

# load pickle files an
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Page Title
st.title('Movie Recommender System')
# Search and selection bar
movie_selection = st.selectbox(
    'Type or select a movie from the dropdown', movies['title'].values)
# display selected option
st.write('You selected:', movie_selection)


# access posters
def fetch_details(movie_id):
    """This function fetches the posters of the recommended movies
    through API token by using Movie_ID set by TMDB"""
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# core function
def get_recommendation(movie_name):
    """This function filter the input movie name to get index within the dataframe.
    Then, feeds the index to similarity matrix to locate the top 5 movies with the closest
     distance range within the dimensional plane."""
    index = movies[movies['title'] == movie_name].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []  # movie list
    recommended_movie_posters = []  # movie poster list
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_details(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movie_posters


# display recommendations according to selected option
if st.button('Show Recommendations'):
    recommended_movies, recommended_movie_posters = get_recommendation(movie_selection)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movies[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movies[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movies[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movies[4])
        st.image(recommended_movie_posters[4])
