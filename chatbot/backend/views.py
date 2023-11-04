from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def chatbot(request):

    if(request.method == "POST"):
        data = json.loads(request.body.decode('utf-8'))
        message = data.get('message')
        response = "This is a test reponse. It should actually be from OPEN AI API"
        return JsonResponse({'message': message, 'response': response})

    return render(request,"chatbox.html")

