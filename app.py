import streamlit as slt
import pickle
import requests

api_key = slt.secrets["tmdb"]["api_key"]

headers = {
    "accept": "application/json",
    "Authorization": api_key
}

def getPosterPath(id):
    url = f"https://api.themoviedb.org/3/movie/{id}"
    response = requests.get(url, headers=headers)
    data=response.json()
    poster_path = data.get("poster_path")  # Extract poster path
    if poster_path:
        return f"https://image.tmdb.org/t/p/original{poster_path}"  # Return full URL
    else:
        return None

# Load data
similarity = pickle.load(open('similartiy.pkl', 'rb'))
movies_df = pickle.load(open('movies.pkl', 'rb'))  # Keep as DataFrame
movies_list = movies_df['title'].values  # Extract titles for dropdown


# Recommendation function
def recommend(movie):
    movie_data = movies_df[movies_df['title'] == movie]
    if movie_data.empty:  # Handle case where movie is not found
        return ["Movie not found!"]

    movie_id = movie_data.index[0]
    movie_selected = list(enumerate(similarity[movie_id]))
    movie_dis = sorted(movie_selected, key=lambda x: x[1], reverse=True)[1:6]

    return [(movies_df.iloc[i[0]]['title'],movies_df.iloc[i[0]]['id']) for i in movie_dis] # i[0] return index


# Streamlit UI
slt.title("Movie Recommender")
selected_movie = slt.selectbox("Search Movie", movies_list)

if slt.button("Recommend"):
    recommendations = recommend(selected_movie)
    cols = slt.columns(5)
    for idx, (movie_name, movie_id) in enumerate(recommendations):  # Limit to 5 movies
        with cols[idx]:
            slt.write(movie_name)  # Display movie title
            poster_url = getPosterPath(movie_id)  # Get poster image
            if poster_url:
                slt.image(poster_url)  # Show poster
            else:
                slt.write("Poster not available.")