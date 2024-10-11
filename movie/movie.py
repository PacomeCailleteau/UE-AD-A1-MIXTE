from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response, render_template
import requests
import resolvers as r

PORT = 3001
HOST = '0.0.0.0'
app = Flask(__name__)


# Elements for Ariadne
type_defs = load_schema_from_path('movie.graphql')
query = QueryType()
movie = ObjectType('Movie')
query.set_field('movie_by_id', r.get_movie_with_id)
query.set_field('movies', r.get_movies)
query.set_field('movies_by_director', r.movies_by_director)
query.set_field('sort_movies_by_rating', r.sort_movies_by_rating)
query.set_field('get_help', r.get_help)

mutation = MutationType()
mutation.set_field('update_movie_rate', r.update_movie_rate_ez)
mutation.set_field("create_movie", r.create_movie)

actor = ObjectType('Actor')
movie.set_field('actors', r.resolve_actors_in_movie)

schema = make_executable_schema(type_defs, movie, actor, query, mutation)


# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


# graphql entry points
@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=None,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

@app.route('/movies', methods=['GET'])
def movies():
    query_movies = '''
    query {
        movies {
            id
            title
            director
            rating
            actors {
                firstname
                lastname
                birthyear
            }
        }
    }
    '''
    response = requests.post('http://127.0.0.1:3001/graphql', json={'query': query_movies})
    movies_data = response.json().get('data', {}).get('movies', [])

    return render_template('movies.html', movies=movies_data)

@app.route('/help', methods=['GET'])
def help_page():
    help_info = r.get_help(None, None)
    return render_template('help.html', help_info=help_info)

if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
