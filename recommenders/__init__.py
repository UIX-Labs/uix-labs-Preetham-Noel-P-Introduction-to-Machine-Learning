import pandas as pd
import numpy as np
import os

print(os.getcwd())

default_poster_url = "https://gurukul-be.s3.ap-south-1.amazonaws.com/0c3df9f4dc56471d88bb88255bb79548.jpg"



data_ratings =pd.read_csv("data_files/ratings.csv") 
data_movies = pd.read_csv( "data_files/movies.csv") 
data_posters = pd.read_csv("data_files/movie_poster.csv") 

data_movies = pd.merge(data_movies, data_posters, how="left", on="movieId")
