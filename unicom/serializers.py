from rest_framework import serializers
from .models import unicom_transaction

class unicom_TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = unicom_transaction
        fields = ['user_phone_number','user_service_provider','recipient','recipient_service_provider','ammount',]