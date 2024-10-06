import json


def get_movie_data():
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        return movies

def get_movies(_, info):
    movies = get_movie_data()
    return movies['movies']

def movie_with_id(_,info,_id):
        movies = get_movie_data()
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

def update_movie_rate_ez(_,info,_id,_rate):
    newmovies = {}
    newmovie = {}
    movies = get_movie_data()
    for movie in movies['movies']:
        if movie['id'] == _id:
            movie['rating'] = _rate
            newmovie = movie
            newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile, indent=2)
    return newmovie

def resolve_actors_in_movie(film, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        result = [actor for actor in actors['actors'] if film['id'] in actor['films']]
        return result

def create_movie(_,info, _id, _title, _director, _rating):
    movies = get_movie_data()
    newmovie = {
        "id": _id,
        "title": _title,
        "director": _director,
        "rating": _rating
    }
    if _id in [movie['id'] for movie in movies['movies']]:
        return None
    movies['movies'].append(newmovie)
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(movies, wfile, indent=2)
    return newmovie

def movies_by_director(_,info,_director):
    movies = get_movie_data()
    return [movie for movie in movies['movies'] if movie['director'] == _director]
