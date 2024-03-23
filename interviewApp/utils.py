from django.conf import settings
import openai
import json
from lmiApp.models import *
from openai import OpenAI
from django.forms.models import model_to_dict
client = OpenAI(api_key = settings.OPEN_AI_SECRET_KEY)

def parse_question_set(question_set_str):
    try:
        question_set_list = question_set_str.split("\n")
        questions = {}
        for question_str in question_set_list:
            if question_str:
                question_number, question = question_str.split(". ", 1)
                questions[question_number.strip()] = question.strip()
        return questions
    except Exception as e:
        print(e)


def generateQuestion(request,msg):
    try:
        body = json.loads(request.body)
        interview_id = body.get("interview_id")
        candidate_id = request.session.get("ID")
        interview = Interview.objects.filter(id = interview_id).first()
        if not interview:
            msg["message"] = "The interview doesn't exists"
            msg["status"] = 400
            return msg
        
        interview_details = InterviewDetail.objects.filter(candidate__id = candidate_id, interview__id = interview_id).first()
        if not interview_details:
            msg["message"] = "You don't have the permissions to be here"
            msg["status"] = 400
            return msg
        
        if interview_details.is_attempted:
            msg["message"] = "You have already appeared for the test"
            msg["status"] = 400
            return msg
        role = interview.role
        exp = interview.yoe
        jd = interview.jd

        prompt = f'I am assigning you the role of interviewer. You need to hire for the role of {role} having {exp} years of experience. Here is the job description for the role you are hiring  : "{jd}". You need to ask 15 questions keeping sticking to the role and job description. The topic of each questions should be diversified and with mixed difficulty level. Also include real world questions to make it look like a real interview. Return questions in json format with question number as key and question as value - This is strict. Also, questions should be such that the answers to it can be categorized to correct, incorrect or partially correct category.'
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=300
        )
        question_set_str = response.choices[0].text
        questions = parse_question_set(question_set_str)
        print(questions)
        interview_details.questions = questions
        interview_details.is_attempted = True
        interview_details.save()
        msg["message"] = questions
        msg["success"] = True
        msg["status"] = 200
        return msg
    except Exception as e:
        msg["message"]  =str(e)
        msg["status"] = 500
        return msg


