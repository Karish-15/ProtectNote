from rest_framework import serializers

from .models import Notes

class NoteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['uniqueID', 'content', 'language', 'public', 'protected']
    