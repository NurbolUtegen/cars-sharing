from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Car, Rental
from .forms import RentalForm
from django.shortcuts import render
from .models import Car

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'myapp/car_list.html', {'cars': cars})


def car_list(request):
    cars = Car.objects.filter(available=True)
    return render(request, "myapp/car_list.html", {"cars": cars})

@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user
            rental.car = car
            rental.total_price = (rental.end_date - rental.start_date).days * car.price_per_day
            rental.save()
            car.available = False
            car.save()
            return redirect("car_list")
    else:
        form = RentalForm()

    return render(request, "myapp/rent_car.html", {"form": form, "car": car})

