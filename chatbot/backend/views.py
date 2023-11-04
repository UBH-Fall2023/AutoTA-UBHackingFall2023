from django.shortcuts import render
from . import chatbox

# Create your views here.
def chatbot(request):
    return render(request, chatbox.html)