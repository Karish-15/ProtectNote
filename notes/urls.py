from django.urls import path

from . import views

urlpatterns = [
    path('create', views.NoteCreateAPIView.as_view(), name='create_note'),
    path('all', views.NotesListAPIView.as_view(), name="all_notes"),
    path('<slug:uniqueID>', views.NoteRetrieveAPIView.as_view(), name="view_note_id"),
    path('<slug:uniqueID>/edit', views.NoteUpdateDestroyAPIView.as_view(), name="edit_note"),
    path('<slug:uniqueID>/getpassword', views.NoteGetPassword.as_view(), name="note_get_password"),
    
]

