from recommenders import data_movies, data_ratings, default_poster_url
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from recommenders.content_based import matching_score



def collaborative_recommendation(movie):

    movies = data_movies.copy()
    def get_title_from_index(index):
        return movies[movies.index == index]['title'].values[0]
    # a function to convert title to index
    def get_index_from_title(title):
        return movies[movies.title == title].index.values[0]
    
    # a function to return the most similar title to the words a user type
    def find_closest_title(title):
        leven_scores = list(enumerate(movies['title'].apply(matching_score, b=title)))
        sorted_leven_scores = sorted(leven_scores, key=lambda x: x[1], reverse=True)
        closest_title = get_title_from_index(sorted_leven_scores[0][0])
        distance_score = sorted_leven_scores[0][1]
        return closest_title, distance_score
    

    closest_title, distance_score = find_closest_title(movie)
    response = []
    # When a user does not make misspellings
    if distance_score == 100:
            
        title_string = f"Here\'s the list of movies similar to {str(closest_title)} \n"
    else:
        title_string =  f'Did you mean {str(closest_title)} ?\n Here\'s the list of movies similar to {str(closest_title)} \n'

    

    ######################################################################################################################################################################
    
    # Combining the data on same column: data_ratings and movies using pivot table => movies_df
    movies_df= pd.pivot_table(data_ratings, values='rating', index='movieId', columns='userId', fill_value=0)
    # Now converting into metrix
    movies_df_metrix= csr_matrix(movies_df.values)
    # Building the model
    model_knn= NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
    model_knn.fit(movies_df_matrix)
    # Fitting the model 
    
    ##########################################################################################################################################################


    index_value = movies_df.index.get_loc(closest_title)
    # Now we will try to find the movies related to select_random_movies
    distances, indices = model_knn.kneighbors(movies_df.iloc[index_value,:].values.reshape(1,-1), n_neighbors= 21)

    sorted_indices = np.argsort(distances.flatten())[::-1]
    sorted_distances = distances.flatten()[sorted_indices]
    sorted_neighbor_indices = indices.flatten()[sorted_indices]
    
    response = []
    for i in range(0, len(sorted_distances)):
        if i == 0:
            #print('Recommendations for {0}:\n'.format(movies_df.index[index_value])) # For which movies it selected
            pass
        else:
            title = movies_df.index[sorted_neighbor_indices[i]]
            movie_record = data_movies[data_movies.title == title].iloc[0]
            movie_poster = str(movie_record.poster_link)
            response.append({
                                    "movieId": int(movie_record.movieId),
                                    "title": str(title),
                                    "image": movie_poster if movie_poster != "nan" else default_poster_url,
                                    "genres": str(movie_record.genres).split("|")
                                })

            #print('{0}: {1}, with distance of {2}:'.format(i, movies_df.index[sorted_neighbor_indices[i]], sorted_distances[i]))

    return {"status": True, "data": {"message": title_string, "results": response}}