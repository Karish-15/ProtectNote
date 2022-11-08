from django.urls import path
from . import views

urlpatterns = [
    path('giveuser', views.giveUserFromTokenAPIView.as_view()),
    path('register', views.registerUserAPIView.as_view(), name='register-user'),
    
]
