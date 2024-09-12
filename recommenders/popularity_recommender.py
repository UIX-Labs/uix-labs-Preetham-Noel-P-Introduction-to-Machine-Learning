from recommenders import data_movies, data_ratings, default_poster_url
import pandas as pd


def recommend_popular_movies():    
    movies_ratings_merged = pd.merge(data_movies, data_ratings, on='movieId')
    movie_ratings = movies_ratings_merged.groupby('title')['rating'].mean().sort_values(ascending=False).head(20).to_dict()
    for movie in movie_ratings:
        movie_record = data_movies[data_movies.title == movie].iloc[0]
        movie_poster = None
        response.append({
            "movieId": int(movie_record.movieId),
            "title": str(movie),
            "image": movie_poster if movie_poster != "nan" or movie_poster else default_poster_url,
            "genres": str(movie_record.genres).split("|"),
            "average_rating": movie_ratings[movie]
        })
    return {"status": True, "data": {"message": "Here are some of the popular recommendations.", "results" : response}}
