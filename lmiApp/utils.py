import json
from .models import *
from lmiApp.models import Organisation
from django.forms.models import model_to_dict
import pandas as pd
from django.core.mail import send_mail

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
            hr_id = request.sesson.get("ID")
            user = CustomUser.objects.get(id = hr_id)
            organisation = Organisation.objects.get(hr = user)
            interview = Interview.objects.create(title =  title, yoe = yoe, organisation = organisation)
            result = model_to_dict(interview)
            msg["status"] = 200
            msg["msg"] = result
            return msg
                
    except Exception as e:
        msg["success"] = False
        msg["msg"] = str(e)
        msg["status"] = 500
        return msg

def invite(request,msg,event):
    try:
        body = json.loads(request.body)
        if event == "invite":
            csv_file = request.FILES.get('csv_file')

            if csv_file is None:
                msg["msg"] = 'No CSV file provided'
                msg["status"] = 400
                return msg
            
            df = pd.read_csv(csv_file)
            invited_count = 0
            for email in df['email']:
                send_mail('Invitation', 'You are invited!', 'from@example.com', [email])
                invited_count += 1
            
            msg["msg"] = f"{invited_count} invitations sent successfully"
            msg["status"] = 200
            return msg

        elif event == "reminder":
            interview_id = body.get("interiew_id")
            interview_data = InterviewDetail.objects.filter(interview__id = interview_id)
            reminder_count = 0
            for element in interview_data:
                if not element.is_attempted:
                    send_mail('Reminder', 'This is reminder for you to appear for a test!', 'from@example.com', [element.candidate.email])
                    reminder_count += 1
            msg["msg"] = f"{reminder_count} reminders sent successfully"
            msg["status"] = 200
            return msg

    except Exception as e:
        msg["success"] = False
        msg["msg"] = str(e)
        msg["status"] = 500
        return msg


def invitation(request,msg,event):
    try:
        body = json.loads(request.body)
        interview_id = body.get("title")
        candidate_id = request.session.get("ID")
        interview_details = InterviewDetail.objects.filter(interview__id=interview_id, candidate__id=candidate_id)
        if interview_details.is_accepted:
            msg["msg"] = "You have already accepted the invitation"
            msg["status"] = 400
            return msg
        if event == "accept":
            interview_details.is_accepted = True
            interview_details.save()
            msg["msg"] = "Bravo ! You are one step closer to your dream job"
            msg["status"] = 200
            return msg
            
        elif event == "decline":
            interview_details.is_declined = True
            interview_details.save()
            msg["msg"] = "We just lost a gem candidate"
            msg["status"] = 200
            return msg
            
    except Exception as e:
        msg["success"] = False
        msg["msg"] = str(e)
        msg["status"] = 500
        return msg