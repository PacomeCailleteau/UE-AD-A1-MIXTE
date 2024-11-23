from pymongo import MongoClient
from graphql import GraphQLError

# Crée un décorateur pour vérifier si l'utilisateur est admin (pas utilisé encore,
# car pas encore de distinction entre admin et user).
def is_admin(func):
    def wrapper(*args, **kwargs):
        context = args[1].context
        if not context.get("role") == "admin": # On vérifie si l'utilisateur est admin
            raise GraphQLError("Accès interdit : droits insuffisants.") # Sinon, on lève une erreur
        return func(*args, **kwargs)
    return wrapper

def get_movies_collection():
    client = MongoClient("mongodb://localhost:27017/") # On récupère le client mongodb
    db_name = client["tpmixte"] # On récupère la base de données du tp
    collection = db_name["movies"] # On récupère la collection movies
    return collection

# Récupère les données de la collection movies
def get_movies_data(collection):
    return list(collection.find())

# Récupère les données de la collection actors
def get_actors_data():
    client = MongoClient("mongodb://localhost:27017/")
    db_name = client["tpmixte"]
    collection = db_name["actors"]
    return list(collection.find())

movies_collection = get_movies_collection() #movie collection sera utile lorsqu'on voudra faire des update, create, delete
movies_db = get_movies_data(movies_collection) # Ensuite, on stocke le find() dans une variable pour éviter de faire des requêtes à chaque fois
actors_db = get_actors_data()

# Récupère la liste des films
def get_movies(_, info):
    return movies_db

# Récupère un film avec son ID
def get_movie_with_id(_, info, _id):
    for movie in movies_db:
        if movie['id'] == _id:
            return movie

# Récupère les acteurs qui ont joué dans le film.
def resolve_actors_in_movie(film, info):
    result = [actor for actor in actors_db if film['id'] in actor['films']] # On filtre les acteurs par film
    return result

# Récupère les films d'un réalisateur
def movies_by_director(_, info, _director):
    return [movie for movie in movies_db if movie['director'] == _director] # On filtre les films par réalisateur

# Trie les films par note (meilleur ou pire)
def sort_movies_by_rating(_, info, order):
    if order not in ['best', 'worst']: # On vérifie si l'ordre est valide
        raise ValueError("The order must be either 'best' or 'worst'.") # Sinon, on lève une erreur

    sorted_movies = sorted(movies_db, key=lambda movie: movie['rating'], reverse=(order == 'best')) # On trie les films par note
    return sorted_movies

# Crée un film
def create_movie(_, info, _id, _title, _director, _rating):
    new_movie = {
        "id": _id,
        "title": _title,
        "director": _director,
        "rating": _rating
    }

    if _id in [movie['id'] for movie in movies_db]: # On vérifie si l'id est déjà utilisé
        raise ValueError("This id is already used.") # Si oui, on lève une erreur

    # on ajoute le film à la liste movies_db en plus de la base de données pour ne pas à refaire un find()
    movies_db.append(new_movie)
    movies_collection.insert_one(new_movie)
    return new_movie

# Met à jour la note d'un film
def update_movie_rate(_, info, _id, _rate):
    updated_movie = None

    for movie in movies_db:
        if movie['id'] == _id:
            movie['rating'] = _rate
            updated_movie = movie
            break

    if updated_movie: # Si le film a été trouvé
        movies_collection.update_one({"id": _id}, {"$set": {"rating": _rate}}) # On le met à jour
        return updated_movie
    else: # Sinon, on lève une erreur
        raise ValueError(f"Aucun film trouvé avec l'ID {_id}")

# Supprime un film
def delete_movie(_, info, _id):
    movie_to_delete = next((movie for movie in movies_db if movie['id'] == _id), None) # récupère le film à supprimer ou None si aucun film n'est trouvé

    if not movie_to_delete: # Si le film n'existe pas
        raise ValueError(f"Aucun film trouvé avec l'ID: {_id}") # On lève une erreur

    movies_db.remove(movie_to_delete)
    movies_collection.delete_one({"id": _id})
    return f"Film avec l'ID {_id} supprimé avec succès."

# Liste les requêtes et mutations disponibles
def get_help(_, info):
    # on sépare les queries des mutations
    help_info = {
        'Queries': [],
        'Mutations': []
    }

    for field_name, field in info.schema.query_type.fields.items(): # On récupère les queries
        query_info = {
            'name': field_name,
            'arguments': []
        }

        if field.args: # Si la query a des arguments
            for arg_name, arg in field.args.items(): # On les récupère
                query_info['arguments'].append({
                    'name': arg_name,
                    'type': str(arg.type)
                })

        help_info['Queries'].append(query_info) # On ajoute les queries à la liste

    if info.schema.mutation_type: # Si on a des mutations
        for field_name, field in info.schema.mutation_type.fields.items(): # On les récupère
            mutation_info = {
                'name': field_name,
                'arguments': []
            }
            if field.args: # Si la mutation a des arguments
                for arg_name, arg in field.args.items(): # On les récupère
                    mutation_info['arguments'].append({
                        'name': arg_name,
                        'type': str(arg.type)
                    })

            help_info['Mutations'].append(mutation_info) # On ajoute les mutations à la liste

    return help_info
