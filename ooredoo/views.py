from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .serializers import ooredoo_SoldeSerializer as SoldeSerializer
from .serializers import ooredoo_TransactionSerializer as TransactionSerializer 
from authentication.models import User
from ooredoo.models import  solde, transaction
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

"""
@api_view(['POST'])
def create_solde(request):
    serializer = SoldeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

class SoldeListAPIView(ListCreateAPIView):
    serializer_class = SoldeSerializer
    queryset = solde.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SoldeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SoldeSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = solde.objects.all()
    lookup_field = "id"

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
                                                
        user_solde = solde.objects.get(phone_number=user_phone_number)
        recipient_solde = solde.objects.get(phone_number=recipient)
        
        # Update user solde
        user_solde.solde -= ammount
        user_solde.save()
        
        # Update recipient solde
        recipient_solde.solde += ammount
        recipient_solde.save()
        
        # Save the transaction
        new_transaction = transaction.objects.create(user=request.user,user_phone_number=user_phone_number ,recipient=recipient, ammount=ammount)
        
        transaction_data = {
            
            
            'user_phone_number': new_transaction.user_phone_number,
            'recipient': new_transaction.recipient,
            'ammount': new_transaction.ammount,
            'updated_at': new_transaction.updated_at,
            'created_at': new_transaction.created_at
        }
        
        return Response(transaction_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
