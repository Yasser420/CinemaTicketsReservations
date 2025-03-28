
from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from .views import RegisterUserView ,AddAdminView , SuperAdminUsersView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/register/', RegisterUserView.as_view()),
    path('admins/adding/', AddAdminView.as_view()), 
    path('users/',SuperAdminUsersView.as_view() ) ,
    path('users/<int:pk>/',SuperAdminUsersView.as_view() )
    
]
