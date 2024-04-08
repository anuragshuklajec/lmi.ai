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
        print(question_set_list)
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

        prompt = f'I am assigning you the role of interviewer. You need to hire for the role of {role} having {exp} years of experience. Here is the job description for the role you are hiring  : "{jd}". You need to ask 15 questions keeping sticking to the role and job description. The topic of each questions should be related to the concepts of technologies mentioned in job description and with mixed difficulty level.. Also include real world questions to make it look like a real interview. Return questions in this format -  "question number. and question, for example 1. Question details" - This is strict. Also, questions should be such that the answers to it should be objective ie., can be categorized can be correct or incorrect'
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=300
        )
        question_set_str = response.choices[0].text
        questions = parse_question_set(question_set_str)
        interview_details.questions = questions
        # interview_details.is_attempted = True
        interview_details.save()
        msg["message"] = questions
        msg["success"] = True
        msg["status"] = 200
        return msg
    except Exception as e:
        msg["message"]  =str(e)
        msg["status"] = 500
        return msg

def answerQuestion(request,msg):
    try:
        body = json.loads(request.body)
        interview_id = body.get("interview_id")
        answers = body.get("answers")
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
        interview_details.answers = answers
        interview_details.save()
        msg["message"] = "You have completed the AI interview process"
        msg["success"] = True
        msg["status"] = 200
        return msg
        
    except Exception as e:
        msg["message"]  =str(e)
        msg["status"] = 500
        return msg

def evaluate(questions,answers):
    prompt = f"I am assigning you the role of interviewer.I will provide you json data of questions and answers. Each key corresponds to specific pair of questions and it's respective answer given by the canidate during the interview. You need to evaluate each questions and it's answer and give it one of following ratings : 0: 'Couldn't provide correct answer or no answer exists', 1 : 'Answer was completely unrrelated to the question', 3: 'Answered in the complete direction but not completely correct.', 4:'Answered in the complete direction but not completely correct',5 : 'Answered correctly' Here's the json data of questions : {questions} and here is respective json data of answers : {answers}. Make sure you return response in json format with question number as key and it's rating as value. Make sure to check if the answers exists or not and rate accordingly and also return the response only in desired format or else you'll be penalised"
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=300
    )
    question_set_str = response.choices[0].text
    print(question_set_str)


def evaluation(request,msg):
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
        
        questions = interview_details.questions
        answers = interview_details.answers

        if not questions or not answers:
            msg["message"] = "Something went wrong, please contact administrator!"
            msg["status"] = 400
            return msg
        
        evaluate(questions,answers)

        msg["message"] = "You have completed the AI interview process"
        msg["success"] = True
        msg["status"] = 200
        return msg
        
    except Exception as e:
        msg["message"]  =str(e)
        msg["status"] = 500
        return msg
