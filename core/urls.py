from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import RegistrationView, HomeView, LoginUserView, LogoutUserView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
