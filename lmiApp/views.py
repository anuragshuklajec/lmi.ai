# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import QuestionRequest
from .config.openai_config import OPENAI_API_KEY
import openai
import json
from .constants import PROMPT_FOR_GENERATING_QUESTIONS

openai.api_key = OPENAI_API_KEY


def home(request):
    if request.method == "GET":
        result = {"result": "Hi, everyone"}
        return JsonResponse(result, status=200, safe=False)


@csrf_exempt
def get_questions(request) -> JsonResponse:
    if request.method == 'POST':
        if request.method == 'POST':
            request_data = json.loads(request.body)
            question_request = QuestionRequest(**request_data)
            question_request.full_clean()

            technology = question_request.technology
            difficulty = question_request.difficulty
            experience = question_request.experience
            number_of_questions = question_request.number_of_questions

            prompt = PROMPT_FOR_GENERATING_QUESTIONS.format(
                number_of_questions,
                difficulty,
                technology,
                experience
            )
            generated_questions = ask_ques_evaluate_ans(prompt).split('\n')

            return JsonResponse({'generated_questions': generated_questions})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def ask_ques_evaluate_ans(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=250,  # You can adjust this based on your needs
        n=1
    )

    return response.choices[0].text.strip()
    # return "openAi responses"
