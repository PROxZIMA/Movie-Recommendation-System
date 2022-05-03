import streamlit as st
from streamlit.proto.RootContainer_pb2 import SIDEBAR
from simple_recommender_system import *
from content_based import *
from indian_movies import *

st.title("Movie Recommendation System")


recommendation_type = st.sidebar.selectbox(
    "Recommendation Type",
    ("Hollywood Genre Based", "Movie Based", "Indian Genre Based"),
)


if recommendation_type == "Hollywood Genre Based":
    genre_selected = st.sidebar.selectbox(
        "Please select any one genre",
        genres(),
    )

    count1 = st.sidebar.number_input(
        "Please enter the count of movies you want!",
        min_value=5,
        max_value=30,
        value=10,
        step=1,
    )
    st.text(" ")
    st.dataframe(build_chart(genre_selected, count1))
    st.text(" ")
    st.write(
        "You can find the dataset & analysis .py file for the above analysis [here](https://drive.google.com/drive/folders/1AjFdtPMa-_4N8pJMV74ATukujDFSg_k_?usp=sharing)"
    )

elif recommendation_type == "Movie Based":
    title = st.sidebar.selectbox(
        "Movie title",
        movie_titles(),
    )
    count2 = st.sidebar.number_input(
        "Please enter the count of movies you want!",
        min_value=5,
        max_value=20,
        value=10,
        step=1,
    )
    st.dataframe(get_recommendations(title, count2))
    st.write(
        "You can find the dataset & analysis .py file for the above analysis [here](https://drive.google.com/drive/folders/1Xz9dLomsYNZe5L90ANHDYEsdrsczhRrT?usp=sharing)"
    )
    st.sidebar.text(" ")
    st.sidebar.text("PS - Please enter the movie title correctly.")
    st.sidebar.text("If error occurs, check for spelling & try again.")

else:
    genre_selected_2 = st.sidebar.selectbox(
        "Please select any one genre",
        genres_im(),
    )

    lang_selected = st.sidebar.selectbox(
        "Please select the language",
        language_im(),
    )
    count3 = st.sidebar.number_input(
        "Please enter the count of movies you want!",
        min_value=5,
        max_value=20,
        value=10,
        step=1,
    )
    st.text(" ")
    st.dataframe(indian_genre_based(genre_selected_2, lang_selected, count3))
