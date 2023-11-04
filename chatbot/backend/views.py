from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

# Create your views here.
def chatbot(request):

    return render(request,"chatbox.html")

