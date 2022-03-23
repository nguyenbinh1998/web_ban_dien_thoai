from django import views
from django.urls import path
from . import views
urlpatterns = [
    path('store/', views.store, name="product_list"),
    path('store/<slug:category_slug>/', views.store, name="product_list_by_category"),
    path('<int:product_id>/<slug:product_slug>/', views.product_detail, name="product_detail"),
    path('remove/<int:product_id>/', views.remove, name="remove"),
    path('cart/', views.cart, name="cart"),
]