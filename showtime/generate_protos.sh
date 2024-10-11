rm showtime_pb2.py
rm showtime_pb2_grpc.py
python3 -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. showtime.proto