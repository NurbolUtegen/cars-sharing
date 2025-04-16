from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.db import transaction
from django.db.models import Prefetch

from .models import Car, Rental
from .forms import RentalForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def car_list(request):
    cars = cache.get('cars_list')
    if not cars:
        cars = Car.objects.filter(available=True).prefetch_related(
            Prefetch('rental_set', queryset=Rental.objects.select_related('user'))
        )
        cache.set('cars_list', list(cars), timeout=60 * 15)
    return render(request, "myapp/car_list.html", {"cars": cars})

@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car.objects.prefetch_related('rental_set'), id=car_id)
    if not car.available:
        return render(request, "myapp/error.html", {"message": "Эта машина уже недоступна."})
    if request.method == "POST":
        form = RentalForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                car.refresh_from_db()
                if not car.available:
                    return render(request, "myapp/error.html", {"message": "Машина уже арендована другим пользователем."})
                rental = form.save(commit=False)
                rental.user = request.user
                rental.car = car
                rental_days = (rental.end_date - rental.start_date).days
                rental.total_price = rental_days * car.price_per_day
                rental.save()
                car.available = False
                car.save()
                return redirect('checkout_page', rental_id=rental.id)
    else:
        form = RentalForm()
    return render(request, "myapp/rent_car.html", {"form": form, "car": car})

def checkout_page(request, rental_id):
    rental = get_object_or_404(Rental.objects.select_related('car', 'user'), id=rental_id)
    return render(request, 'myapp/checkout.html', {
        'rental': rental,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })

@csrf_exempt
def create_checkout_session(request, rental_id):
    rental = get_object_or_404(Rental.objects.select_related('car'), id=rental_id)
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(rental.total_price * 100),
                    'product_data': {'name': f'Rental of {rental.car.model}'},
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{settings.DOMAIN}/success/',
            cancel_url=f'{settings.DOMAIN}/cancel/',
            metadata={'rental_id': str(rental.id)}
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)




