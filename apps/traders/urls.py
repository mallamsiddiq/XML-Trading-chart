# userdashboard/urls.py
from django.urls import path
from .views import DasboardView, TraderDasboardView, AllTradersView

from django.views import defaults

urlpatterns = [
    path('dashboard/<int:trader_id>/', TraderDasboardView.as_view(), name='chart'),
    path('dashboard', DasboardView.as_view(), name='dashboard'),
    path('home', AllTradersView.as_view(), name='home'),
    
    path('', AllTradersView.as_view(), name='home')
]
