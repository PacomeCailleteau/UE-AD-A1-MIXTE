import json
from graphql import GraphQLObjectType

def get_movie_data():
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        return movies

def get_movies(_, info):
    movies = get_movie_data()
    return movies['movies']

def get_movie_with_id(_, info, _id):
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
        raise ValueError("This id is already used.")
    movies['movies'].append(newmovie)
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(movies, wfile, indent=2)
    return newmovie

def movies_by_director(_,info,_director):
    movies = get_movie_data()
    return [movie for movie in movies['movies'] if movie['director'] == _director]

def sort_movies_by_rating(_, info, order):
    movies = get_movie_data()

    if order not in ['best', 'worst']:
        raise ValueError("The order must be either 'best' or 'worst'.")

    sorted_movies = sorted(movies['movies'], key=lambda movie: movie['rating'], reverse=(order == 'best'))
    return sorted_movies

def get_help(_, info):
    help_info = {
        'Queries': [],
        'Mutations': []
    }

    for field_name, field in info.schema.query_type.fields.items():

        query_info = {
            'name': field_name,
            'arguments': []
        }

        if field.args:
            for arg_name, arg in field.args.items():
                query_info['arguments'].append({
                    'name': arg_name,
                    'type': str(arg.type)
                })

        help_info['Queries'].append(query_info)

    if info.schema.mutation_type:
        for field_name, field in info.schema.mutation_type.fields.items():
            mutation_info = {
                'name': field_name,
                'arguments': []
            }
            if field.args:
                for arg_name, arg in field.args.items():
                    mutation_info['arguments'].append({
                        'name': arg_name,
                        'type': str(arg.type)
                    })

            help_info['Mutations'].append(mutation_info)

    return help_info

def delete_movie(_, info, _id):
    movies = get_movie_data()
    movie_to_delete = None

    for movie in movies['movies']:
        if movie['id'] == _id:
            movie_to_delete = movie
            break

    if not movie_to_delete:
        raise ValueError(f"Aucun film trouvé avec l'ID: {_id}")

    movies['movies'].remove(movie_to_delete)

    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(movies, wfile, indent=2)

    return f"Film avec l'ID {_id} supprimé avec succès."
