from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(default=2000)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Rental: {self.car} by {self.user}"


