from django.urls import path
from .views import TopUpOrderCreateAPIView, dashboard_view

urlpatterns = [
    path('api/topup/', TopUpOrderCreateAPIView.as_view(), name='topup-create'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
