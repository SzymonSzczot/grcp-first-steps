import grpc

from basics.protos.generated.route_guid_pb2 import Point
from basics.protos.generated.route_guid_pb2 import Rectangle
from basics.protos.generated.route_guid_pb2 import RouteNote
from basics.protos.generated.route_guid_pb2_grpc import RouteGuideStub

channel = grpc.insecure_channel("localhost:50051")
stub = RouteGuideStub(channel)

# Standard
point = Point(lng=10, lat=12)
feature = stub.GetFeature(point)
print("Sync " + str(feature))

# Async
feature_future = stub.GetFeature.future(point)
feature = feature_future.result()
print("Async " + str(feature))

rectangle = Rectangle(lo=Point(lng=10, lat=5), hi=Point(lng=14, lat=10))
for feature in stub.ListFeatures(rectangle):
    print(feature)

point_iterator = (p for p in [Point(lng=10, lat=5), Point(lng=11, lat=6), Point(lng=12, lat=7)])
route_summary = stub.RecordRoute(point_iterator)

sent_route_note_iterator = [
    RouteNote(point=Point(lng=10, lat=5), message="start"),
    RouteNote(point=Point(lng=12, lat=6), message="middle"),
    RouteNote(point=Point(lng=15, lat=7), message="end")
]
for received_route_note in stub.RouteChat(sent_route_note_iterator):
    print(received_route_note)
