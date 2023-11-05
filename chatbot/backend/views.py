from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .AutoTA import AutoTA

# Create your views here.
@csrf_exempt
def login_view(request):
    if(request.method == 'POST'):

        return redirect('chatbot')

    return render(request, 'login.html')


@csrf_exempt
def chatbot(request):
    myAutoTA = AutoTA(corpus_folders_path=r"./backend/secret_stuff/data", api_key_path=r"./backend/secret_stuff/OPENAI_API_KEY.txt")

    if (request.method == "POST"):
        input_box = json.loads(request.body.decode('utf-8'))
        user_input = input_box['message']

        html_response, user_input, filepaths_of_relevent_docs, total_tokens_used = myAutoTA.ask(user_input=user_input)

        print(f"User Input: {user_input}")
        print(f"Total Tokens Used: {total_tokens_used}")
        print(f"Filepaths of Relevent Docs: {filepaths_of_relevent_docs}")
        print(f"System Response: {html_response}")

        return JsonResponse({'message': user_input, 'response': html_response, 'refrences': filepaths_of_relevent_docs, 'total_tokens_used': total_tokens_used})

    return render(request, "chatbox.html")


