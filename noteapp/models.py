import re
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Note(models.Model):
    u_id=models.ForeignKey(User,on_delete=models.CASCADE)
    note_name=models.CharField(max_length=225)
    description=models.TextField()
    current_time=models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.u_id.username

TITLE_CHOICES = [
    ('1', 'Normal_user'),
    ('2', 'Employee'),
]

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    # image = models.FileField(null=True, blank=True)
    address= models.TextField(max_length=1000)
    intrest=models.CharField(max_length=100)
    dob=models.DateField()
    date_added=models.DateField(auto_now_add=True)
    user_type= models.CharField(max_length=20,choices=TITLE_CHOICES)

    def __str__(self):
        return self.user.username

