from django.shortcuts import render
from .models import Guest , Movie , Reservation
from django.http.response import JsonResponse 
from .serializers import MovieSerializer ,ReservationSerializer , GuestSerializer
from django.http import Http404
from rest_framework.response import Response 
from rest_framework import status ,  viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from fuzzywuzzy import process
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

class CBV_PK(APIView):
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        guest=self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
    
 #use view sets for my CRUD operations   
class  guest_CRUD(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
class  movie_CRUD(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class  reservation_CRUD(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
@api_view(['GET'])
def find_movie(request):
   user_search = request.data['name']
   movies = Movie.objects.values_list('name',flat=True)
   best_movie_result , score = process.extractOne(user_search , movies)
   if score > 60 : 
       suggested_movies = Movie.objects.filter(name = best_movie_result) 
       serializer = MovieSerializer(suggested_movies , many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
   return Response({"message": "No similar movie found"}, status=status.HTTP_404_NOT_FOUND)

