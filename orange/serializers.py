from rest_framework import serializers
from .models import orange_solde as solde,orange_transaction as transaction

class orange_SoldeSerializer(serializers.ModelSerializer):

    class Meta:
        model = solde
        fields = ['solde', 'phone_number']
      
class orange_TransactionSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = transaction
            fields = ['recipient','ammount','user_phone_number']

