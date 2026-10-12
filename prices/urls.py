from django.urls import path

from . import views

app_name = 'prices'

urlpatterns = [
    path('', views.price_list, name='price-list'),
    path('<int:price_id>/', views.price_detail, name='price-detail'),
]