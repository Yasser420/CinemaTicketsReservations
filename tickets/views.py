from django.shortcuts import render
from .models import Guest
from django.http.response import JsonResponse 
from .serializers import MovieSerializer ,ReservationSerializer , GuestSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.
#function based view 
#the get_guests_rest function is used for both GET and POST methods for the same endpoint with different business logic
@api_view(['GET','POST'])
def get_guests(request):
     #if the request is GET method
     if request.method== 'GET': 
         guests= Guest.objects.all()
         serializer = GuestSerializer(guests,many=True)
         return Response(serializer.data , status=status.HTTP_200_OK)
     elif request.method == 'POST':    
       serializer = GuestSerializer(data=request.data)
       #if the request data is valid
       if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
       #if request data is not valid
       return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
       
