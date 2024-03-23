from authentication.decorators import check_session
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import *

@check_session
@csrf_exempt
def startTest(request):
    """get lists of questions for a candidate"""
    msg={"success": False, "message": "", "status" : 200}
    if request.method == "POST":
        result = generateQuestion(request,msg)
        return JsonResponse(data = result, status = result["status"], safe=False)
    else:
        msg["message"] = "Invalid method"
        msg["status"] = 400
        msg["success"] = False
        return JsonResponse(data = result, status = msg["status"], safe=False)
