from django.urls import path

from webapp.views import (
    ProductListView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductUpdateView,
    CartAddView, CartView, CartDeleteView, CartDeleteOneView, OrderCreate
)

app_name = "webapp"

urlpatterns = [
    path('', ProductListView.as_view(), name="index"),
    path('articles/add/', ProductCreateView.as_view(), name="product_add"),
    path('article/<int:pk>/', ProductDetailView.as_view(), name="product_view"),
    path('article/<int:pk>/update/', ProductUpdateView.as_view(), name="product_update"),
    path('article/<int:pk>/delete/', ProductDeleteView.as_view(), name="product_delete"),
    path('article/<int:pk>/add-cart/', CartAddView.as_view(), name="product_add_cart"),
    path('cart/', CartView.as_view(), name="cart"),
    path('cart/<int:pk>/remove/', CartDeleteView.as_view(), name="delete_from_cart"),
    path('cart/<int:pk>/remove-one/', CartDeleteOneView.as_view(), name="delete_from_cart_one"),
    path('order/create/', OrderCreate.as_view(), name="order_create"),

]
