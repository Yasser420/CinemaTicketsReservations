from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
   ROLE_CHOICES = [
       ('user' , 'User') , 
       ('admin','Admin') , 
       ('super admin' , 'Super Admin')
   ]
   role = models.CharField(max_length=20 , choices=ROLE_CHOICES , default='user')

class Movie(models.Model):
    name=models.CharField(max_length=20)
    release_date =models.DateField(auto_now_add=True)
    duration=models.PositiveIntegerField(help_text="Duration in minutes")
    
class Reservation(models.Model):
    user=models.ForeignKey(User, related_name='reservation',on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie, related_name='reservation',on_delete=models.CASCADE)
    reservation_date=models.DateTimeField(null=False)