import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
from pymongo import MongoClient

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    # Set up the connection
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/") # On récupère le client mongodb
        self.db_name = self.client["tpmixte"] # On récupère la base de données du tp
        self.collection = self.db_name["times"] # On récupère la collection times
        self.db = list(self.collection.find()) #On transforme le find() en liste d'objet

    # Get a showtime by a date
    def GetShowtimeByDate(self, request, context):
        for showtime in self.db:
            if showtime['date'] == request.date:
                print("Showtime found!")
                return showtime_pb2.ShowtimeData(date=showtime['date'], movies=showtime['movies'])
        return showtime_pb2.ShowtimeData(date="", movies=[])


    # get all the showtimes
    def GetListShowtimes(self, request, context):
        for showtime in self.db:
            yield showtime_pb2.ShowtimeData(date=showtime['date'], movies=showtime['movies'])


# start the server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()