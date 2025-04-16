from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet
from django.urls import path
from . import views





urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
]

router = DefaultRouter()
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]