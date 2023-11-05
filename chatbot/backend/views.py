from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt





# Create your views here.
@csrf_exempt
def login_view(request):
    if(request.method == 'POST'):

        return redirect('chatbot')

    return render(request, 'login.html')


@csrf_exempt
def chatbot(request):

    if(request.method == "POST"):
        data = json.loads(request.body.decode('utf-8'))
        message = data.get('message')
        response = "This is a test reponse. It should actually be from OPEN AI API"
        return JsonResponse({'message': message, 'response': response, 'refrences': []})

    return render(request,"chatbox.html")


