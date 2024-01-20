from rest_framework import serializers
from .models import solde ,transaction

class ooredoo_SoldeSerializer(serializers.ModelSerializer):

    class Meta:
        model = solde
        fields = ['solde', 'phone_number']
      
class ooredoo_TransactionSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = transaction
            fields = ['recipient','ammount','user_phone_number']

