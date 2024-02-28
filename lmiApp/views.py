from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
from .utils import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def register(request):
    msg={"success": False, "message": "", "status" : 200}
    if request.method == "POST":
        data = json.loads(request.body)
        msg = createAccount(data,msg)
        return JsonResponse(data=msg,status=msg["status"],safe=False)

@csrf_exempt
def auth_login(request):
    msg={"success": False, "message": "", "status" : 200}
    if request.method == "POST":
        data = json.loads(request.body)
        msg = login(data,msg,request)
        return JsonResponse(data = msg,safe=False,status=msg["status"])

@csrf_exempt
def auth_logout(request):
    msg={"success": False, "message": "", "status" : 200}
    if request.method == "POST":
        msg = logout(msg,request)
        return JsonResponse(data = msg,safe=False,status=msg["status"])



        
        


