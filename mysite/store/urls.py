from django.urls import path
from store import views

urlpatterns = [
    path('products/', views.ListProducts.as_view()),
]