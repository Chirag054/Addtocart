from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('signup/', views.UserCreate.as_view(), name='register'),
    path('signin/', views.UserLogin.as_view(), name='login'),
]
