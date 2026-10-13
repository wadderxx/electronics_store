from django.urls import path

from .views import (
    CartView,
    CartItemView,
    ClearCartView,
)

urlpatterns = [
    path('', CartView.as_view()),
    path('items/<int:item_id>/', CartItemView.as_view()),
    path('clear/', ClearCartView.as_view()),
]