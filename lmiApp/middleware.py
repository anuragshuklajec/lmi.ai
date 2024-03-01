# middleware.py
from django.core.exceptions import ValidationError
from django.http import JsonResponse


def handle_exception(request, exception):
    # Handle specific types of exceptions if needed
    if isinstance(exception, ValueError):
        return JsonResponse({'error': f'ValueError: {exception}'}, status=400)
    elif isinstance(exception, KeyError):
        return JsonResponse({'error': f'KeyError: {exception}'}, status=400)
    elif isinstance(exception, ValidationError):
        return JsonResponse({'error': f'ValidationError: {exception}'}, status=400)
    # Handle other exceptions
    return JsonResponse({'error': 'An unexpected error occurred'}, status=500)


class GlobalExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        return handle_exception(request, exception)
