from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def home(request):
    if request.method == "GET":
        result = {"result" : "Hi, everyone"}
        return JsonResponse(result, status=200, safe=False)

