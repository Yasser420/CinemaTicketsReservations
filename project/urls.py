
from django.contrib import admin
from django.urls import path , include
from tickets import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests', views.guest_CRUD)
router.register('movies', views.movie_CRUD)
router.register('reservations', views.reservation_CRUD)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/movie', views.find_movie) , 
    # path('guests/', views.guests.as_view()),
    # path('guests/<int:pk>',views.CBV_PK().as_view())
    path('api1/', include(router.urls))
   
]
