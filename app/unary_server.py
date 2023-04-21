from concurrent import futures
import grpc
import requests
from util import is_api_healthy, settings


import professional_unary_pb2_grpc as pb2_grpc
import professional_unary_pb2 as pb2
from urllib.parse import urljoin


class UnaryService(pb2_grpc.ProfessionalUnaryServicer):
    def __int__(self, *args, **kwargs):
        ...

    def GetProContactInfo(self, request, context):

        if not is_api_healthy():
            return None

        contact_details_method_url = f"api/pro/{request.pro_id}/contact_info/"
        api_domain = settings.get_api_url()
        url = urljoin(api_domain, contact_details_method_url)
        response = requests.get(url)
        result = response.json()

        return pb2.ContactDetails(**result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ProfessionalUnaryServicer_to_server(UnaryService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
