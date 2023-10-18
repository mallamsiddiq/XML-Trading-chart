from django.urls import path
from .views import RegisterView, AuthLoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('login/', AuthLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Add more authentication-related URLs as needed
]