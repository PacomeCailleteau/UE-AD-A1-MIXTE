# REST API

# CALLING gRPC requests
import json

import grpc
from flask import Flask


class UserServicer(user_pb2_grpc.UserServicer):

   def __init__(self):
      with open('{}/data/users.json'.format("."), "r") as jsf:
         self.db = json.load(jsf)["users"]

   def write(users):
      data = {"users": users}
      with open('./data/users.json', 'w') as f:
         json.dump(data, f, indent=2)


   def getUsers(self, request, context):
      for user in self.db:
         yield user_pb2.BookingData(id=user['id'], name=user['name'], lastactivite=user["last_activite"])


   def GetUserById(self, request, context):
      for user in self.db:
         if user['userid'] == request.userid:
            print("User found!")
            return user_pb2.UserData(id=user['id'], name=user['name'], lastactivite=user["last_activite"])
      return user_pb2.UserData(id="", name="", lastactivite="")

   def AddUser(self, request, context):
      ## vérif que l'item n'extiste pas déjà
      user = getUserById(userid)
      if not request.id in request.id:
         return user_pb2.UserData(id="", name="", lastactivite="")
      # ajout dans la bdd
      write(self.db)
      return user_pb2.UserData(id=user['id'], name=user['name'], lastactivite=user["last_activite"])

   # TO DO
   def EditUser(self, request, context):

   # TO DO
   def DeleteUser(self, request, context):

   # TO DO
   def getBookingsOfUser(userId):
      with grpc.insecure_channel('localhost:3001') as channel:
         stub = booking_pb2_grpc.BookingStub(channel)
         booking_date = booking_pb2_grpc.UserId(userid=userId)
         response = stub.GetBookingByUserID(booking_date)
         return response

# CALLING GraphQL requests
# todo to complete

app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
