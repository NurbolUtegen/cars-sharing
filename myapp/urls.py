from django.urls import path
from . import views

urlpatterns = [
    path("", views.car_list, name="car_list"),
    path("rent/<int:car_id>/", views.rent_car, name="rent_car"),
]
