from django.urls import path
from django.contrib.auth import views as auth_views
from myapp.views import car_list, rent_car, checkout_page, create_checkout_session

urlpatterns = [
    # Маршруты для аутентификации
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Страница входа
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Страница выхода

    # Остальные маршруты твоего приложения
    path('', car_list, name='car_list'),
    path('rent/<int:car_id>/', rent_car, name='rent_car'),
    path('checkout/<int:rental_id>/', checkout_page, name='checkout_page'),
    path('create-checkout-session/<int:rental_id>/', create_checkout_session, name='create_checkout_session'),
]

