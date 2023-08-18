from django.urls import path

from . import views

urlpatterns = [
    path('create', views.NoteCreateAPIView.as_view(), name='create-note'),
    path('all', views.NotesListAPIView.as_view()),
    path('<slug:uniqueID>', views.NoteRetrieveAPIView.as_view()),
    path('<slug:uniqueID>/edit', views.NoteUpdateDestroyAPIView.as_view()),
    path('<slug:uniqueID>/getpassword', views.NoteGetPassword.as_view()),
    
]

