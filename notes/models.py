import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User as User_object_model

User = settings.AUTH_USER_MODEL

class Notes(models.Model):
    uniqueID = models.UUIDField(unique=True, null = False, default = uuid.uuid4, editable=False)
    content = models.TextField(max_length = 2000)
    language = models.TextField(max_length=20, default = "text")
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    public = models.BooleanField(default = False)
    protected = models.BooleanField(default = False)
    password = models.TextField(default = (User_object_model.objects.make_random_password(length=15) if protected else None))

    def is_public(self) -> bool:
        return self.public
    
    def is_protected(self) -> bool:
        return self.protected