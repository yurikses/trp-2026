from django.urls import path

from . import views

urlpatterns = [
    path('', views.price_list, name='price-list'),
    path('<int:price_id>/', views.price_detail, name='price-detail'),
]