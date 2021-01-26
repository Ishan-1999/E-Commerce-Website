from django.urls import path
from . import views

urlpatterns = [
    path('thrift/', views.thrift, name="thrift"),
    path('diy/', views.diy, name="diy"),
    path('fnd/', views.fnd, name="fnd"),
    path('local/', views.local, name="local"),
    path('', views.home, name="home"),
    path("products/<int:myId>", views.productView, name="productView"),
    path('contact/', views.contact, name="contact"),
    path('cartview/', views.cartview, name="cartview"),
    path('checkout/', views.checkout, name="checkout"),
    path('tracker/', views.tracker, name="tracker"),
    path('search/', views.search, name="search"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path("success/", views.payu_success, name="payu_success"),
    path("failure/", views.payu_failure, name="payu_failure"),
]
