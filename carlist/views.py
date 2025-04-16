from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import viewsets
from .models import Car
from .serializers import CarSerializer
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # перенаправление на login после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    return render(request, 'home.html')

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer