from django.shortcuts import render
from .models import Guest
from django.http.response import JsonResponse 
from .serializers import MovieSerializer ,ReservationSerializer , GuestSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
# Create your views here.
#function based view 
#the get_guests_rest function is used for both GET and POST methods for the same endpoint with different business logic
# @api_view(['GET','POST'])
# def get_guests(request):
#      #if the request is GET method
#      if request.method== 'GET': 
#          guests= Guest.objects.all()
#          serializer = GuestSerializer(guests,many=True)
#          return Response(serializer.data , status=status.HTTP_200_OK)
#      elif request.method == 'POST':    
#        serializer = GuestSerializer(data=request.data)
#        #if the request data is valid
#        if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#        #if request data is not valid
#        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
         
# #GET PUT DELETE
# @api_view(['GET','PUT','DELETE'])
# def guest(request, pk):
#     try:
#       _guest=Guest.objects.get(pk=pk)
#     except Guest.DoesNotExist:
#          return Response(status=status.HTTP_404_NOT_FOUND)    
#     if request.method== 'GET':
#       serializer=GuestSerializer(_guest)
#       return Response(serializer.data)
#     elif request.method=='PUT':
#       serializer=GuestSerializer(_guest,data=request.data)
#       if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
#       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     elif request.method=='DELETE':
#          _guest.delete()
#          return Response(status=status.HTTP_204_NO_CONTENT)




#use class based views for GET List and POST object

#get list of guests
class guests(APIView):
     def get(self, request): 
         guests=Guest.objects.all()
         serializer=GuestSerializer(guests,many=True)
         return Response(serializer.data,status=status.HTTP_200_OK)
     
     def post(self,request):
         serializer=GuestSerializer(data=request.data)   
         if serializer.is_valid():
              serializer.save()
              return Response(serializer.data,status=status.HTTP_201_CREATED)
         return Response({"errors": serializer.errors},status=status.HTTP_400_BAD_REQUEST)  