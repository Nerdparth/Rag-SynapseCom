from django.db import models
from django.contrib.auth.models import User
import uuid 

class Bots(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=250, blank=False, null=False)
    file = models.FileField(upload_to="files/", blank=True ,null=True)
    filename = models.CharField(max_length=500, blank=False, null=False)
    vectordb_path = models.CharField(max_length=200, blank=False, null=False)

class Response(models.Model):
    bot = models.ForeignKey(Bots, on_delete=models.CASCADE)
    query = models.CharField(max_length=500, blank=False, null=False)
    response_generated = models.CharField(max_length=1000, blank=False, null=False)