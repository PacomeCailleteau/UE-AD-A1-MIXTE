import json
from graphql import GraphQLError

def is_admin(func):
    def wrapper(*args, **kwargs):
        context = args[1].context
        if not context.get("role") == "admin":
            raise GraphQLError("Accès interdit : droits insuffisants.")
        return func(*args, **kwargs)
    return wrapper

def get_movie_data():
    with open('./data/movies.json', "r") as file:
        movies = json.load(file)
        return movies


def write(movies):
    data = {"movies": movies}
    with open('./data/movies.json', 'w') as f:
        json.dump(data, f, indent=4)


def get_movies(_, info):
    movies = get_movie_data()
    return movies['movies']


def get_movie_with_id(_, info, _id):
    movies = get_movie_data()
    for movie in movies['movies']:
        if movie['id'] == _id:
            return movie


def update_movie_rate(_, info, _id, _rate):
    movies = get_movie_data()['movies']
    updated_movie = None

    for movie in movies:
        if movie['id'] == _id:
            movie['rating'] = _rate
            updated_movie = movie
            break

    if updated_movie:
        write(movies)
        return updated_movie
    else:
        raise ValueError(f"Aucun film trouvé avec l'ID {_id}")


def resolve_actors_in_movie(film, info):
    with open('./databases/actors.json', "r") as file:
        actors = json.load(file)
        result = [actor for actor in actors['actors'] if film['id'] in actor['films']]
        return result


def create_movie(_, info, _id, _title, _director, _rating):
    movies = get_movie_data()['movies']
    new_movie = {
        "id": _id,
        "title": _title,
        "director": _director,
        "rating": _rating
    }

    if _id in [movie['id'] for movie in movies]:
        raise ValueError("This id is already used.")

    movies.append(new_movie)
    write(movies)
    return new_movie


def movies_by_director(_, info, _director):
    movies = get_movie_data()
    return [movie for movie in movies['movies'] if movie['director'] == _director]


def sort_movies_by_rating(_, info, order):
    movies = get_movie_data()['movies']

    if order not in ['best', 'worst']:
        raise ValueError("The order must be either 'best' or 'worst'.")

    sorted_movies = sorted(movies, key=lambda movie: movie['rating'], reverse=(order == 'best'))
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
    movies = get_movie_data()['movies']
    movie_to_delete = next((movie for movie in movies if movie['id'] == _id), None)

    if not movie_to_delete:
        raise ValueError(f"Aucun film trouvé avec l'ID: {_id}")

    movies.remove(movie_to_delete)
    write(movies)
    return f"Film avec l'ID {_id} supprimé avec succès."
