from django.urls import path
from . import views

urlpatterns = [
    path('boys/', views.boys, name="boys"),
    path('', views.home, name="home"),
    path('girls/', views.girls, name="girls"),
    path("products/<int:myId>", views.productView, name="productView"),
    path('contact/', views.contact, name="contact"),
    path('cartview/', views.cartview, name="cartview"),
    path('checkout/', views.checkout, name="checkout"),
    path('tracker/', views.tracker, name="tracker")
]
