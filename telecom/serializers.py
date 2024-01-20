from rest_framework import serializers
from .models import telecom_solde as solde,telecom_transaction as transaction

class SoldeSerializer(serializers.ModelSerializer):

    class Meta:
        model = solde
        fields = ['solde', 'phone_number']
      
class TransactionSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = transaction
            fields = ['recipient','ammount','user_phone_number']

