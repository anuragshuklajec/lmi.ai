import json
from .models import *
from lmiApp.models import Organisation
from django.forms.models import model_to_dict
import pandas as pd
from django.core.mail import send_mail
from datetime import datetime,timedelta

def organisation(request,msg,event):
    try:
        if event == "create":
            body = json.loads(request.body)
            name = body.get("title")
            hr_id = request.session.get("ID")
            user = CustomUser.objects.get(id = hr_id)
            organisation = Organisation.objects.create(name = name, hr = user)
            result = model_to_dict(organisation)
            msg["success"] = True
            msg["status"] = 200
            msg["msg"] = result
            return msg
    except Exception as e:
        msg["success"] = False
        msg["msg"] = str(e)
        msg["status"] = 500
        return msg
    
def interview(request,msg,event):
    try:
        body = json.loads(request.body)
        if event == "create":
            title = body.get("title")
            yoe = body.get("yoe")
            hr_id = request.session.get("ID")
            user = CustomUser.objects.get(id = hr_id)
            organisation = Organisation.objects.get(hr = user)
            interview = Interview.objects.create(title =  title, yoe = yoe, organisation = organisation)
            result = model_to_dict(interview)
            msg["success"] = True
            msg["status"] = 200
            msg["msg"] = result
            return msg
                
    except Exception as e:
        msg["msg"] = str(e)
        msg["status"] = 500
        return msg

def invite(request,msg,event):
    try:
        if event == "invite-many":
            interview_id = request.POST.get('interview_id')
            interview = Interview.objects.get(id = interview_id)
            csv_file = request.FILES.get('csv_file')

            if csv_file is None:
                msg["msg"] = 'No CSV file provided'
                msg["status"] = 400
                return msg
            
            df = pd.read_csv(csv_file)
            invited_count = 0
            for email in df['email']:
                createInterviewDetailObject(email,interview)
                send_mail('Invitation', f'You are invited for {interview.title}!', 'from@example.com', [email])
                invited_count += 1

            msg["success"] = True
            msg["msg"] = f"{invited_count} invitations sent successfully"
            msg["status"] = 200
            return msg
        
        body = json.loads(request.body)
        interview_id = body.get("interview_id")
        if event == "invite-one":
            email = body.get("email")
            interview = Interview.objects.get(id = interview_id)
            createInterviewDetailObject(email,interview)
            send_mail('Invitation', f"You are invited for {interview.title}!", 'from@example.com', [email])
            msg["success"] = True
            msg["msg"] = f"invitations sent successfully"
            msg["status"] = 200
            return msg

        elif event == "reminder":
            interview_data = InterviewDetail.objects.filter(interview__id = interview_id)
            reminder_count = 0
            for element in interview_data:
                if not element.is_attempted:
                    send_mail('Reminder', 'This is reminder for you to appear for a test!', 'from@example.com', [element.email])
                    reminder_count += 1
            msg["success"] = True
            msg["msg"] = f"{reminder_count} reminders sent successfully"
            msg["status"] = 200
            return msg

    except Exception as e:
        msg["msg"] = str(e)
        msg["status"] = 500
        return msg


def invitation(request,msg,event):
    try:
        body = json.loads(request.body)
        interview_id = body.get("interview_id")
        candidate_id = request.session.get("ID")
        interview_details = InterviewDetail.objects.filter(interview__id=interview_id, candidate__id=candidate_id).first()
        if not interview_details:
            msg["msg"] = "You are not authorized to be here"
            msg["status"] = 400
            return msg
        if interview_details.is_accepted:
            msg["msg"] = "You have already accepted the invitation"
            msg["status"] = 400
            return msg
        if event == "accept":
            interview_details.is_accepted = True
            interview_details.save()
            msg["success"] = True
            msg["msg"] = "Bravo ! You are one step closer to your dream job"
            msg["status"] = 200
            return msg
            
        elif event == "decline":
            interview_details.is_declined = True
            interview_details.save()
            msg["success"] = True
            msg["msg"] = "We just lost a gem candidate"
            msg["status"] = 200
            return msg
            
    except Exception as e:
        msg["msg"] = str(e)
        msg["status"] = 500
        return msg
    
def createInterviewDetailObject(email,interview):
    candidate = CustomUser.objects.filter(email = email).first()
    expiry = datetime.now() + timedelta(days=5)
    obj, created = InterviewDetail.objects.get_or_create(email = email,candidate = candidate,interview = interview)
    if created:
        obj.expiry = expiry
        obj.save()


