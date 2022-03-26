import time

from basics.protos.generated import route_guid_pb2_grpc
from basics.protos.generated.route_guid_pb2 import Feature
from basics.protos.generated.route_guid_pb2 import Point
from basics.protos.generated.route_guid_pb2 import RouteSummary


class RouteGuideServicer(route_guid_pb2_grpc.RouteGuideServicer):

    db = [
        Feature(location=Point(lng=10, lat=12), name="1")
    ]

    @classmethod
    def get_feature(cls, request):
        db = cls.db
        return Feature(name="feature", location=request)

    @classmethod
    def get_distance(cls, prev_point, point):
        return 10

    def GetFeature(self, request, context):
        feature = self.get_feature(request)
        if feature is None:
            return Feature(name="", location=request)
        else:
            return feature

    def ListFeatures(self, request, context):
        for feature in self.db:
            yield feature

    def RecordRoute(self, request_iterator, context):
        for point in request_iterator:
            print(point)
        return RouteSummary(
            point_count=1,
            feature_count=2,
            distance=int(3),
            elapsed_time=int(3)
        )

    def RouteChat(self, request_iterator, context):
        prev_notes = []
        for new_note in request_iterator:
            for prev_note in prev_notes:
                if prev_note.location == new_note.location:
                    yield prev_note
            prev_notes.append(new_note)
