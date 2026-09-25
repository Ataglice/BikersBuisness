from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('moto-service/', views.new_service_view, name='moto_service'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('contacts/', views.conctacts_view, name='contacts'),
    path('submit-callback/', views.submit_callback, name='submit_callback'),
]