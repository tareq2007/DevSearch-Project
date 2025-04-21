from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    username =models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    p_image = models.ImageField(upload_to='profiles/',default='profiles/udf.png', null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    social_github= models.CharField(blank=True, null=True, max_length=200)
    social_youtube= models.CharField(blank=True, null=True, max_length=200)
    social_website= models.CharField(blank=True, null=True, max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)

    def __str__(self):
        return self.username
    class Meta:
        ordering = ['created']


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)


    def __str__(self):
        return self.name
    

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)


    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['is_read','-created']



