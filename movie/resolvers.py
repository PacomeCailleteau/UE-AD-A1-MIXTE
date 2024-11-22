from pymongo import MongoClient
from graphql import GraphQLError

def is_admin(func):
    def wrapper(*args, **kwargs):
        context = args[1].context
        if not context.get("role") == "admin":
            raise GraphQLError("Accès interdit : droits insuffisants.")
        return func(*args, **kwargs)
    return wrapper

def get_movies_collection():
    client = MongoClient("mongodb://localhost:27017/") # On récupère le client mongodb
    db_name = client["tpmixte"] # On récupère la base de données du tp
    collection = db_name["movies"] # On récupère la collection movies
    return collection

def get_movies_data(collection):
    return list(collection.find())

def get_actors_data():
    client = MongoClient("mongodb://localhost:27017/")
    db_name = client["tpmixte"]
    collection = db_name["actors"]
    return list(collection.find())

movies_collection = get_movies_collection() #movie collection sera utile lorsqu'on voudra faire des update, create, delete
movies_db = get_movies_data(movies_collection) # Ensuite, on stocke le find() dans une variable pour éviter de faire des requêtes à chaque fois
actors_db = get_actors_data()

def get_movies(_, info):
    return movies_db

def get_movie_with_id(_, info, _id):
    for movie in movies_db:
        if movie['id'] == _id:
            return movie


def update_movie_rate(_, info, _id, _rate):
    updated_movie = None

    for movie in movies_db:
        if movie['id'] == _id:
            movie['rating'] = _rate
            updated_movie = movie
            break

    if updated_movie:
        # update du film pour la base de données mongodb
        movies_collection.update_one({"id": _id}, {"$set": {"rating": _rate}})
        return updated_movie
    else:
        raise ValueError(f"Aucun film trouvé avec l'ID {_id}")


def resolve_actors_in_movie(film, info):
    # on récupère les acteurs qui ont joué dans le film
    result = [actor for actor in actors_db if film['id'] in actor['films']]
    return result


def create_movie(_, info, _id, _title, _director, _rating):
    new_movie = {
        "id": _id,
        "title": _title,
        "director": _director,
        "rating": _rating
    }

    if _id in [movie['id'] for movie in movies_db]:
        raise ValueError("This id is already used.")

    # on ajoute le film à la liste movies_db en plus de la base de données pour ne pas à refaire un find()
    movies_db.append(new_movie)
    movies_collection.insert_one(new_movie)
    return new_movie


def movies_by_director(_, info, _director):
    return [movie for movie in movies_db if movie['director'] == _director]


def sort_movies_by_rating(_, info, order):
    if order not in ['best', 'worst']:
        raise ValueError("The order must be either 'best' or 'worst'.")

    sorted_movies = sorted(movies_db, key=lambda movie: movie['rating'], reverse=(order == 'best'))
    return sorted_movies


def get_help(_, info):
    # on sépare les requêtes des mutations
    help_info = {
        'Queries': [],
        'Mutations': []
    }

    # on récupère les queries pour les ajouter à l'objet help_info
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
        #on récupère les mutations pour les ajouter à l'objet help_info
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
    # récupère le film à supprimer ou None si aucun film n'est trouvé
    movie_to_delete = next((movie for movie in movies_db if movie['id'] == _id), None)

    if not movie_to_delete:
        raise ValueError(f"Aucun film trouvé avec l'ID: {_id}")

    movies_db.remove(movie_to_delete)
    movies_collection.delete_one({"id": _id})
    return f"Film avec l'ID {_id} supprimé avec succès."
