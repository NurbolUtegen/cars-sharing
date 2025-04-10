from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from myapp.views import car_list, rent_car 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cars/', car_list, name='car_list'),
    path('rent/<int:car_id>/', rent_car, name='rent_car'),
]


urlpatterns = [
    path("", views.car_list, name="car_list"),
    path("rent/<int:car_id>/", views.rent_car, name="rent_car"),
]
