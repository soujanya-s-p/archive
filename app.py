import streamlit as st
import pickle
import requests
from huggingface_hub import hf_hub_download

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = "c7ec19ffdd3279641fb606d19ceb9bb1"  # Replace with your TMDB API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    try:
        data = requests.get(url).json()
        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
    
    return "https://via.placeholder.com/200"  # Placeholder image if no poster is available

# Load movies dataset
movies = pickle.load(open("movies_list.pkl", 'rb'))

# Download and load similarity.pkl from Hugging Face
repo_id = "souvani2004/similarity"
filename = "similarity.pkl"

file_path = hf_hub_download(repo_id=souvani2004/similarity, filename=filename, local_dir=".")
with open(file_path, "rb") as f:
    similarity = pickle.load(f)

# Extract movie titles
movies_list = movies['title'].values

# Streamlit App UI
st.title("🎬 Movie Recommender System")

# Movie selection dropdown
selectvalue = st.selectbox("🎥 Select a Movie:", movies_list)

# Recommendation function
def recommend(movie):
    try:
        index = movies.index[movies['title'] == movie][0]  # Get movie index
    except IndexError:
        st.error("⚠️ Movie not found. Please select another one.")
        return [], []
    
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    
    recommend_movie = []
    recommend_poster = []
    
    for i in distance[1:6]:  # Get top 5 similar movies
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    
    return recommend_movie, recommend_poster

# Display recommendations
if st.button("🔍 Show Recommendations"):
    movie_names, movie_posters = recommend(selectvalue)
    
    if movie_names:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.text(movie_names[0])
            st.image(movie_posters[0])
        
        with col2:
            st.text(movie_names[1])
            st.image(movie_posters[1])
        
        with col3:
            st.text(movie_names[2])
            st.image(movie_posters[2])
        
        with col4:
            st.text(movie_names[3])
            st.image(movie_posters[3])
        
        with col5:
            st.text(movie_names[4])
            st.image(movie_posters[4])


