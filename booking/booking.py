import grpc
import showtime_pb2
import showtime_pb2_grpc
import booking_pb2
import booking_pb2_grpc

from concurrent import futures
from pymongo import MongoClient

class BookingServicer(booking_pb2_grpc.BookingServicer):

    # Set up connection
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/") # On récupère le client mongodb
        self.db_name = self.client["tpmixte"] # On récupère la base de données du tp
        self.collection = self.db_name["bookings"] # On récupère la collection bookings
        self.db = list(self.collection.find()) # On stocke les données dans une variable pour éviter de faire des requêtes à chaque fois


    # Get the bookings of a user via his id
    def GetBookingByUserID(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.userid:
                print("Booking found!")
                return booking_pb2.BookingData(userid=booking['userid'], dates=booking['dates'])
        return booking_pb2.BookingData(userid="", dates=[])


    # Get all the bookings
    def GetListBookings(self, request, context):
        for booking in self.db:
            yield booking_pb2.BookingData(userid=booking['userid'], dates=booking['dates'])

    # Add a booking to a user
    def AddBookingToUser(self, request, context):
        ## vérif que l'item n'extiste pas déjà
        date = request.date
        showtime = get_showtime_by_date(date)
        if not request.movie in showtime.movies:
            return booking_pb2.BookingData(userid="", dates=[])

        # ajout dans la bd
        for booking in self.db:
            if booking['userid'] == request.userid:
                # si la date n'existe pas alors on la crée
                if not any(date['date'] == request.date for date in booking['dates']):
                    booking['dates'].append({'date': request.date, 'movies': [request.movie]})
                    self.collection.update_one(
                        {"userid": request.userid},
                        {"$set": {"dates": booking['dates']}})
                    return booking_pb2.BookingData(userid=booking['userid'], dates=booking['dates'])
                # sinon on parcourt la liste pour mettre l'item au bon endroit
                for date in booking['dates']:
                    if date['date'] == request.date:
                        if request.movie in date['movies']:
                            return booking_pb2.BookingData(userid=booking['userid'], dates=booking['dates'])
                        date['movies'].append(request.movie)
                        self.collection.update_one(
                            {"userid": request.userid},
                            {"$set": {"dates": booking['dates']}})
                        return booking_pb2.BookingData(userid=booking['userid'], dates=booking['dates'])

        return booking_pb2.BookingData(userid="", dates=[])

# get the showtimes sorted by date
def get_showtime_by_date(date):
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)
        showtime_date = showtime_pb2.ShowtimeDate(date=date)
        response = stub.GetShowtimeByDate(showtime_date)
        return response

# start the server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
