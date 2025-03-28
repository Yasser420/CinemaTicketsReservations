
from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import  TokenRefreshView
from tickets.views import UserLoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/login/', UserLoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/',include('tickets.urls'))
]
