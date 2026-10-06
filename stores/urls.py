from django.urls import path

from . import views

urlpatterns = [
    path('', views.store_list, name='store-list'),
    path('<int:store_id>/', views.store_detail, name='store-detail'),
]