from django.db import models

# Create your models here.
class Guest(models.Model):
    name=models.CharField(max_length=10)
    phone=models.CharField(max_length=13)

class Movie(models.Model):
    name=models.CharField(max_length=20)
    release_date =models.DateField(auto_now_add=True)
    duration=models.PositiveIntegerField(help_text="Duration in minutes")
    
class Reservation(models.Model):
    guest=models.ForeignKey(Guest, related_name='reservation',on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie, related_name='reservation',on_delete=models.CASCADE)
    reservation_date=models.DateTimeField(null=False)