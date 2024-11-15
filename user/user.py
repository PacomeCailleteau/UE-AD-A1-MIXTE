import json
from lib2to3.fixes.fix_input import context

import grpc
import requests
from flask import Flask, request, jsonify, make_response

import booking_pb2
import booking_pb2_grpc

app = Flask(__name__)

# A VOIR POUR METTRE DANS UN .ENV ?
PORT = 3203
HOST = '0.0.0.0'
BOOKING_SERVICE_URL = "http://localhost:3003/bookings/"
MOVIE_SERVICE_URL = "http://localhost:3200/movies/"

with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]
#with open("UE-archi-distribuees-User-1.0.0-resolved.yaml", "r") as f:
#    openapi_spec = yaml.safe_load(f)

@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=['GET'])
def get_users():
    json = jsonify(users)
    response = make_response(json, 200)
    return response


@app.route("/users", methods=['POST'])
def add_user():
    req = request.get_json()

    for user in users:
        if str(user['id']) == req['id']:
            return make_response(jsonify({'error': 'User ID already exists'}, user), 409)

    users.append(req)
    write(users)

    return make_response(jsonify({"message": "user added"}, req), 200)


@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user['id']) == str(userid):
            return make_response(jsonify(user), 200)
    return make_response(jsonify({'error': 'User not found', "id": userid}), 404)


#Voir pour une meilleure gestion des erreurs
@app.route("/users/<userid>", methods=['PUT'])
def update_user_byid(userid):
    req = request.get_json()

    for user in users:
        if str(user['id']) == str(userid):
            users.remove(user)
            users.append(req)
            write(users)
            return make_response(jsonify({"message": "user updated"},req), 200)
    return make_response(jsonify({'error': 'User not found', "id": userid}), 404)


@app.route("/users/<userid>", methods=['DELETE'])
def del_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            users.remove(user)
            write(users)
            return make_response(jsonify({"message": "user deleted"}, user),200)

    res = make_response(jsonify({"error":"user ID not found", "id": userid}),400)
    return res


# Tous les users triés par leur dernière activité
@app.route("/users/bylastactive", methods=['GET'])
def get_user_bylastactive():
    json = jsonify(users)
    sorted_users_bylastactive = sorted(users, key=lambda user: user.get("last_active", 0))
    response = make_response(sorted_users_bylastactive, 200)
    return response


# récupérer tous les bookings d'un user (lien avec booking)
@app.route("/users/<userid>/bookings", methods=['GET'])
def get_user_bookings(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            try:
                with grpc.insecure_channel('localhost:3003') as channel:
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


# même chose, mais en récupérant aussi les infos des films (lien avec booking et movie)
@app.route("/users/<userid>/bookings/movies", methods=['GET'])
def get_user_bookings_movies(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            try:
                with grpc.insecure_channel('localhost:3003') as channel:
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

                    try:
                        for booking in bookings:
                            for movie in booking["movies"]:
                                print(movie)
                                # FAIRE EN GRAPHQL

                    except grpc.RpcError as e:
                        # Gérez les erreurs gRPC
                        return make_response(jsonify({
                            "error": "Error contacting Booking service",
                            "details": e.details()
                        }), 500)
                    return make_response(jsonify({"userid": response.userid, "bookings": bookings}), 200)

            except grpc.RpcError as e:
                # Gérez les erreurs gRPC
                return make_response(jsonify({
                    "error": "Error contacting Booking service",
                    "details": e.details()
                }), 500)
    return


def write(users):
    data = {"users": users}
    with open('./data/users.json', 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
