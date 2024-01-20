from django.urls import path
from . import views


urlpatterns = [ 
    path('transaction/', views.post, name='create_transaction'),
    path('transactions/', views.TransactionListAPIView.as_view(), name='get_transactions'),
]