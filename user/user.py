import json

import grpc
import requests
from bson import ObjectId
from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient

import booking_pb2
import booking_pb2_grpc

app = Flask(__name__)

# A VOIR POUR METTRE DANS UN .ENV ?
PORT = 3004
HOST = '0.0.0.0'
BOOKING_SERVICE_URL = "localhost:3003"
MOVIE_SERVICE_URL = "http://127.0.0.1:3001/graphql"

def get_users_collection():
    client = MongoClient("mongodb://localhost:27017/")
    db_name = client["tpmixte"]
    collection = db_name["users"]
    return collection

def get_users_data(collection):
    users = list(collection.find())
    return users

users_collection = get_users_collection()
users_db = get_users_data(users_collection)

# Used to serialize ObjectId to string, otherwise it give an error when serializing to JSON
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

# Used to easily convert data to JSON using the custom JSONEncoder
def custom_jsonify(data):
    return json.loads(JSONEncoder().encode(data))

@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=['GET'])
def get_users():
    json = custom_jsonify(users_db)
    response = make_response(json, 200)
    return response


@app.route("/users", methods=['POST'])
def add_user():
    req = request.get_json()

    for user in users_db:
        if str(user['id']) == req['id']:
            return make_response(jsonify({'error': 'User ID already exists'}, custom_jsonify(user)), 409)

    users_db.append(req)
    users_collection.insert_one(req)

    return make_response(jsonify({"message": "user added"}, custom_jsonify(req)), 200)


@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users_db:
        if str(user['id']) == str(userid):
            return make_response(custom_jsonify(user), 200)
    return make_response(jsonify({'error': 'User not found', "id": userid}), 404)


#Voir pour une meilleure gestion des erreurs
@app.route("/users/<userid>", methods=['PUT'])
def update_user_byid(userid):
    req = request.get_json()

    for user in users_db:
        if str(user['id']) == str(userid):
            users_db.remove(user)
            users_db.append(req)
            users_collection.update_one({"id": userid}, {"$set": req})
            return make_response(jsonify({"message": "user updated"}, custom_jsonify(req)), 200)
    return make_response(jsonify({'error': 'User not found', "id": userid}), 404)


@app.route("/users/<userid>", methods=['DELETE'])
def del_user_byid(userid):
    for user in users_db:
        if str(user["id"]) == str(userid):
            users_db.remove(user)
            users_collection.delete_one({"id": userid})
            return make_response(jsonify({"message": "user deleted"}, custom_jsonify(user)),200)

    res = make_response(jsonify({"error":"user ID not found", "id": userid}),400)
    return res


# Tous les users triés par leur dernière activité
@app.route("/users/bylastactive", methods=['GET'])
def get_user_bylastactive():
    sorted_users_bylastactive = sorted(users_db, key=lambda user: user.get("last_active", 0))
    response = make_response(custom_jsonify(sorted_users_bylastactive), 200)
    return response


# récupérer tous les bookings d'un user (lien avec booking)
@app.route("/users/<userid>/bookings", methods=['GET'])
def get_user_bookings(userid):
    for user in users_db:
        if str(user["id"]) == str(userid):
            try:
                with grpc.insecure_channel(BOOKING_SERVICE_URL) as channel:
                    stub = booking_pb2_grpc.BookingStub(channel)
                    request_grpc = booking_pb2.UserId(userid=userid)
                    response = stub.GetBookingByUserID(request_grpc)

                    bookings = [
                        {
                            "date": showtime.date,
                            "movies": list(showtime.movies)  # Convertir RepeatedScalarContainer en liste
                        }
                        for showtime in response.dates
                    ]
                    return make_response(jsonify({"userid": response.userid, "bookings": bookings}), 200)

            except grpc.RpcError as e:
                # Gérez les erreurs gRPC
                return make_response(jsonify({
                    "error": "Error contacting Booking service",
                    "details": e.details()
                }), 500)
    return


# Récupérer les informations de films via leur id en graphQL
def fetch_movie_details(movie_ids):
    """ Fonction pour récupérer les informations des films via GraphQL (un ID à la fois) """
    query = """
    query Movie_by_id($id: String!) {
        movie_by_id(_id: $id) {
            id
            title
            director
            rating
        }
    }
    """

    movie_details = []

    for movie_id in movie_ids:
        variables = {
            "id": movie_id  # Un seul ID à la fois
        }

        response = requests.post(MOVIE_SERVICE_URL, json={'query': query, 'variables': variables})

        if response.status_code == 200:
            # Ajoutez les données du film récupérées à la liste des résultats
            movie_details.append(response.json()["data"]["movie_by_id"])
        else:
            raise Exception(f"GraphQL query failed for ID {movie_id}: {response.text}")

    return movie_details


# même chose, mais en récupérant aussi les infos des films (lien avec booking et movie)
@app.route("/users/<userid>/bookings/movies", methods=['GET'])
def get_user_bookings_movies(userid):
    for user in users_db:
        if str(user["id"]) == str(userid):
            try:
                with grpc.insecure_channel(BOOKING_SERVICE_URL) as channel:
                    stub = booking_pb2_grpc.BookingStub(channel)
                    request_grpc = booking_pb2.UserId(userid=userid)
                    response = stub.GetBookingByUserID(request_grpc)

                    movie_ids = []
                    bookings = []
                    for showtime in response.dates:
                        movies_list = list(showtime.movies)
                        movie_ids.extend(movies_list)
                        bookings.append({
                            "date": showtime.date,
                            "movies": movies_list
                        })

                    # Récupération des informations sur les films
                    movie_details = fetch_movie_details(movie_ids)

                    for booking in bookings:
                        booking["movie_details"] = []
                        for movie in booking["movies"]:
                            movie_info = next(
                                (movie_detail for movie_detail in movie_details if movie_detail["id"] == movie), None)
                            if movie_info:
                                booking["movie_details"].append(movie_info)

                    return make_response(jsonify({"userid": response.userid, "bookings": bookings}), 200)

            except grpc.RpcError as e:
                return make_response(jsonify({
                    "error": "Error contacting Booking service",
                    "details": e.details()
                }), 500)
            except Exception as e:
                return make_response(jsonify({
                    "error": "Error contacting Movie service",
                    "details": str(e)
                }), 500)

    return make_response(jsonify({"error": "User not found"}), 404)

if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
