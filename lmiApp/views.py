from authentication.decorators import hr_required,check_session
from django.views.decorators.csrf import csrf_exempt
from .utils import *
from django.http import JsonResponse

@hr_required
@check_session
@csrf_exempt
def createOrganisation(request):
    """creates organisation"""
    msg={"success": False, "message": "", "status" : 200}
    if request.method == "POST":
        result = organisation(request,msg,"create")
        return JsonResponse(data = result, status = result["status"], safe=False)
    else:
        msg["message"] = "Invalid method"
        msg["status"] = 400
        msg["success"] = False
        return JsonResponse(data = result, status = msg["status"], safe=False)

@hr_required
@check_session
@csrf_exempt
def createInterview(request):
    """creates interview"""
    msg={"success": False, "message": "", "status" : 200}
    if request.method == "POST":
        result = interview(request,msg,"create")
        return JsonResponse(data = result, status = result["status"], safe=False)
    else:
        msg["message"] = "Invalid method"
        msg["status"] = 400
        msg["success"] = False
        return JsonResponse(data = result, status = msg["status"], safe=False)

    
@hr_required
@csrf_exempt
def sendInvites(request):
    """takes in an interview ID and send invites to list of candidates over mail"""
    msg={"success": False, "message": "", "status" : 200}
    if request.method == 'POST':
        event = request.GET.get('event', None)
        if event == "many":
            result = invite(request,msg,"invite-many")
            return JsonResponse(data = result, status = result["status"], safe=False)
        elif event == "single":
            result = invite(request,msg,"invite-one")
            return JsonResponse(data = result, status = result["status"], safe=False)
        else:
            msg["message"] = "Please specify event"
            msg["status"] = 400
            return JsonResponse(data = msg,status = msg["status"], safe = False)

    else:
        msg["message"] = "Invalid method"
        msg["status"] = 400
        msg["success"] = False
        return JsonResponse(data = result, status = msg["status"], safe=False)


@check_session
@csrf_exempt
def acceptInvite(request):
    """allows a candidate to accept interview"""
    msg={"success": False, "message": "", "status" : 200}
    if request.method == 'POST':
        result = invitation(request,msg,"accept")
        return JsonResponse(data = result, status = result["status"], safe=False)

    else:
        msg["message"] = "Invalid method"
        msg["status"] = 400
        msg["success"] = False
        return JsonResponse(data = result, status = msg["status"], safe=False)
    

@check_session
@csrf_exempt
def declineInvite(request):
    """allows a candidate to decline interview"""
    msg={"success": False, "message": "", "status" : 200}
    if request.method == 'POST':
        result = invitation(request,msg,"decline")
        return JsonResponse(data = result, status = result["status"], safe=False)
    else:
        msg["message"] = "Invalid method"
        msg["status"] = 400
        msg["success"] = False
        return JsonResponse(data = result, status = msg["status"], safe=False)

@hr_required
@csrf_exempt
def sendReminder(request):
    """takes a particular interview id and sends reminder to all those who have not appeared"""
    msg={"success": False, "message": "", "status" : 200}
    if request.method == 'POST':
        result = invite(request,msg,"reminder")
        return JsonResponse(data = result, status = result["status"], safe=False)
    else:
        msg["message"] = "Invalid method"
        msg["status"] = 400
        msg["success"] = False
        return JsonResponse(data = result, status = msg["status"], safe=False)