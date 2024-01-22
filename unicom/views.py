from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .serializers import unicom_TransactionSerializer as TransactionSerializer
from authentication.models import User
from .models import unicom_transaction
from ooredoo.models import solde, transaction
from orange.models import orange_solde, orange_transaction
from telecom.models import telecom_solde, telecom_transaction

from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class TransactionListAPIView(ListAPIView):
    serializer_class = TransactionSerializer
    queryset = unicom_transaction.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


@swagger_auto_schema(method='post',request_body=TransactionSerializer)
@api_view(['POST']) 
@permission_classes([IsAuthenticated,IsOwner])
def post(request):
    serializer = TransactionSerializer(data=request.data)
    
    if serializer.is_valid():
        ammount = serializer.validated_data['ammount']
        recipient = serializer.validated_data['recipient']
        user_phone_number = serializer.validated_data['user_phone_number'] 
        user_service_provider=serializer.validated_data['user_service_provider'] 
        recipient_service_provider=serializer.validated_data['recipient_service_provider']
        # Check if the recipient is in the database

        if user_service_provider == 'ooredoo':
            user_solde = solde.objects.get(phone_number=user_phone_number)
        elif user_service_provider == 'orange':
            user_solde = orange_solde.objects.get(phone_number=user_phone_number)
        elif user_service_provider == 'telecom':
            user_solde = telecom_solde.objects.get(phone_number=user_phone_number)

        if recipient_service_provider == 'ooredoo':
            recipient_solde = solde.objects.get(phone_number=recipient)
        elif recipient_service_provider == 'orange':
            recipient_solde = orange_solde.objects.get(phone_number=recipient)
        elif recipient_service_provider == 'telecom':
            recipient_solde = telecom_solde.objects.get(phone_number=recipient)
                                                
        # Update user solde
        user_solde.solde -= ammount
        user_solde.save()
        
        # Update recipient solde
        recipient_solde.solde += ammount
        recipient_solde.save()
        
        # Save the transaction
        new_transaction = unicom_transaction.objects.create(user=request.user, user_phone_number=user_phone_number,
        user_service_provider=user_service_provider, recipient=recipient,recipient_service_provider=recipient_service_provider ,ammount=ammount)
        
        transaction_data = {
            
            
            'user_phone_number': new_transaction.user_phone_number,
            'user_service_provider': new_transaction.user_service_provider,
            'recipient': new_transaction.recipient,
            'recipient_service_provider': new_transaction.recipient_service_provider,
            'ammount': new_transaction.ammount,
            'updated_at': new_transaction.updated_at,
            'created_at': new_transaction.created_at
        }
        
        return Response(transaction_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
