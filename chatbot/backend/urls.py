from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),  # Empty string sets login_view as the home page
    path('/chat',views.chatbot, name="chatbot")
] 