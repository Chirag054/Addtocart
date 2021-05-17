from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartDetail.as_view(), name='cart_detail'),
    path('products/', views.CartItemCreate.as_view(), name='cart_item_create'),
    path('products/<int:pk>/', views.CartItemDetail.as_view(), name='cart_item_detail'),
]