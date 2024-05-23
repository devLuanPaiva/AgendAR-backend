from rest_framework import status
from rest_framework.response import Response

def send_error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({"error": message}, status=status_code)