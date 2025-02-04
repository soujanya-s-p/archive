import streamlit as st
import pickle
import requests
import os


def fetch_poster(movie_id):
     url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
     data=requests.get(url)
     data=data.json()
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
     return full_path

movies = pickle.load(open("movies_list.pkl", 'rb'))
#similarity = pickle.load(open("similarity.pkl", 'rb'))

file_id = "1qk2BkDcK0gL5PjWR04I4K2bqztAZAHi6"
url = f"https://drive.google.com/uc?export=download&id={file_id}"
output = "similarity.pkl"

# Download the file
response = requests.get(url, allow_redirects=True)

# Save the response content
with open(output, "wb") as f:
    f.write(response.content)

# Check file size before unpickling
import os
print("Downloaded file size:", os.path.getsize(output), "bytes")


try:
    with open(output, "rb") as f:
        similarity = pickle.load(f)
    print("✅ similarity.pkl loaded successfully!")
except FileNotFoundError:
    print("❌ ERROR: similarity.pkl not found!")
    similarity = None
except pickle.UnpicklingError:
    print("❌ ERROR: similarity.pkl is corrupted!")
    similarity = None
except Exception as e:
    print("❌ ERROR while loading similarity.pkl:", e)
    similarity = None


movies_list=movies['title'].values

st.header("Movie Recommender System")

import streamlit.components.v1 as components

import streamlit.components.v1 as components
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
   
    ]


selectvalue=st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]
    for i in distance[1:6]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster



if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
