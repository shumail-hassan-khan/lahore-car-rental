from rest_framework.response import Response

def success_response(message, data=None, status_code=200):
    return Response({
        "status": 1,
        "message": message,
        "data": data or {}
    }, status=status_code)

def error_response(message, data=None, status_code=400):
    return Response({
        "status": 0,
        "message": message,
        "data": data or {}
    }, status=status_code)
