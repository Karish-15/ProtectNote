from django.test import TestCase, Client
from django.urls import reverse
from notes.models import Notes
from notes.serializers import NoteModelSerializer 
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class NoteCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass", first_name="test", last_name="user")
        self.note = Notes.objects.create(content="Test note", author=self.user, protected=False, public=False, language="")

        self.client = Client()
        self.client.login(username="testuser", password="testpass")
        
    def test_create_note(self):
        
        data = {"content": "New note", "author": self.user.id, "username": "testuser", "password": "testpass"}
        token = self.client.post(reverse('token_obtain_pair'), data=data).json()["access"]
        token = 'Bearer ' + token
        
        response = self.client.post(reverse("create_note"), data=data, headers={"Authorization": token})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Notes.objects.filter(content="New note").exists())

    def test_create_note_invalid_data(self):
        data = {"author": self.user.id, "username": "testuser", "password": "testpass"}
        token = self.client.post(reverse('token_obtain_pair'), data=data).json()["access"]
        token = 'Bearer ' + token
        
        response = self.client.post(reverse("create_note"), data=data, headers={"Authorization": token})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Notes.objects.filter(author=self.user).exclude(content="Test note").exists())

    def test_private_note_not_available(self):
        self.client.logout()

        data = {"username": "testuser", "password": "testpass"}
        token = self.client.post(reverse('token_obtain_pair'), data=data).json()["access"]
        token = 'Bearer ' + token

        response = self.client.get(reverse('view_note_id', args=[self.note.uniqueID]))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class NoteListAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass", first_name="test", last_name="user")
        self.note = Notes.objects.create(content="Test note", author=self.user, protected=False, public=False, language="")

        self.client = Client()
        self.client.login(username="testuser", password="testpass")

    def test_list_notes(self):
        data = {"username": "testuser", "password": "testpass"}
        token = self.client.post(reverse('token_obtain_pair'), data=data).json()["access"]
        token = 'Bearer ' + token

        response = self.client.get(reverse('all_notes'), headers={"Authorization": token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0]["content"], "Test note")

class NoteRetrieveAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass", first_name="test", last_name="user")
        self.note = Notes.objects.create(content="Test note", author=self.user, protected=False, public=False, language="")
        self.client = Client()
        self.client.login(username="testuser", password="testpass")

    def test_retrieve_note(self):
        data = {"username": "testuser", "password": "testpass"}
        token = self.client.post(reverse('token_obtain_pair'), data=data).json()["access"]
        token = 'Bearer ' + token

        response = self.client.get(reverse('view_note_id', args=[self.note.uniqueID]), headers={"Authorization": token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["content"], "Test note")

class NoteUpdateDestroyAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass", first_name="test", last_name="user")
        self.note = Notes.objects.create(content="Test note", author=self.user, protected=False, public=False, language="")
        self.client = Client()
        self.client.login(username="testuser", password="testpass")

    def test_update_note(self):
        data = {"username": "testuser", "password": "testpass"}
        token = self.client.post(reverse('token_obtain_pair'), data=data).json()["access"]
        token = 'Bearer ' + token

        response = self.client.put(reverse('edit_note', args=[self.note.uniqueID]), data={"content": "Updated note"}, headers={"Authorization": token})

    def test_delete_note(self):
        data = {"username": "testuser", "password": "testpass"}
        token = self.client.post(reverse('token_obtain_pair'), data=data).json()["access"]
        token = 'Bearer ' + token

        response = self.client.delete(reverse('edit_note', args=[self.note.uniqueID]), headers={"Authorization": token})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Notes.objects.filter(content="Test note").exists())

class NoteGetPasswordAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass", first_name="test", last_name="user")
        self.note = Notes.objects.create(content="Test note", author=self.user, protected=True, public=False, language="")
        self.client = Client()
        self.client.login(username="testuser", password="testpass")

    def test_get_password(self):
        data = {"username": "testuser", "password": "testpass"}
        token = self.client.post(reverse('token_obtain_pair'), data=data).json()["access"]
        token = 'Bearer ' + token

        response = self.client.get(reverse('note_get_password', args=[self.note.uniqueID]), headers={"Authorization": token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["password"], self.note.password)






