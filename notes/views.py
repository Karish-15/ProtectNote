from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.response import Response

from .models import Notes
from .serializers import NoteModelSerializer

class NoteCreateAPIView(generics.CreateAPIView):
    queryset = Notes.objects.all()
    serializer_class = NoteModelSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

class NotesListAPIView(generics.ListAPIView):
    serializer_class = NoteModelSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Notes.objects.all().filter(author = self.request.user)

class NoteUpdateDestroyAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = NoteModelSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'uniqueID'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_queryset(self):
        return Notes.objects.all().filter(author=self.request.user)

class NoteRetrieveAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        obj = Notes.objects.get(uniqueID = kwargs['uniqueID'])
        if obj:
            note_serializer = NoteModelSerializer(obj)
            if obj.protected:
                if self.request.user.is_authenticated:
                    pwd = self.request.data.get('password', None)
                    if not pwd:
                        return Response({'error': 'Password required to access protected note'}, status=400)
                                
                    elif pwd == obj.password:
                        return Response(note_serializer.data, status=200)
                    else:
                        return Response({'error': 'Invalid password to access protected note'}, status=400)
                else:
                        return Response({'error': 'User authentication required'}, 400)
            else:
                if obj.public:
                    return Response(note_serializer.data, status=200)
                else:
                    if self.request.user.is_authenticated:
                        if not self.request.user == obj.author:
                            return Response({'error': 'Current user is not the author of the requested note'}, 400)
                        return Response(note_serializer.data, status=200)
                    else:
                        return Response({'error': 'User authentication required'}, 400)
        
        return Response({"error": "uniqueID is invalid"}, status=404)

class NoteGetPassword(views.APIView):
    def get(self, request, *args, **kwargs):
        obj = Notes.objects.get(uniqueID = kwargs['uniqueID'])
        if obj:
            if obj.protected:
                if self.request.user.is_authenticated and self.request.user == obj.author:
                    return Response({'password': obj.password})
            else:
                return Response({"error": "Requested note is unprotected"}, status=400)
        else:
            return Response({"error": "uniqueID is invalid"}, status=404)
