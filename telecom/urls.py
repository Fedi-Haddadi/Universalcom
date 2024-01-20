from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('solde/', views.SoldeListAPIView.as_view(), name='create_solde'),
    path('solde/<int:id>/', views.SoldeDetailAPIView.as_view(), name='solde_detail'),
    path('transaction/', views.post, name='create_transaction'),
]