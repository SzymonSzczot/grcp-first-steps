from concurrent import futures

import grpc

from basics.protos.generated.route_guid_pb2_grpc import add_RouteGuideServicer_to_server
from basics.route_guide_server import RouteGuideServicer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_RouteGuideServicer_to_server(RouteGuideServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

serve()
