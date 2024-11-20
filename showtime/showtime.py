import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
from pymongo import MongoClient

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db_name = self.client["tpmixte"]
        self.collection = self.db_name["times"]
        self.db = list(self.collection.find())

    def GetShowtimeByDate(self, request, context):
        for showtime in self.db:
            if showtime['date'] == request.date:
                print("Showtime found!")
                return showtime_pb2.ShowtimeData(date=showtime['date'], movies=showtime['movies'])
        return showtime_pb2.ShowtimeData(date="", movies=[])

    def GetListShowtimes(self, request, context):
        for showtime in self.db:
            yield showtime_pb2.ShowtimeData(date=showtime['date'], movies=showtime['movies'])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()