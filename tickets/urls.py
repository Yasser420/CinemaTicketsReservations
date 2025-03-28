
from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from .views import RegisterUserView ,AddAdminView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/register/', RegisterUserView.as_view()),
    path('admins/adding/', AddAdminView.as_view())
]
