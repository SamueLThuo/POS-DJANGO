from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-sale/', views.create_sale, name='create_sale'),
    path('receipt/<int:sale_id>/', views.receipt_view, name='receipt'),
]
