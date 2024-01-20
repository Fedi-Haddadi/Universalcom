from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class orange_solde(models.Model):
    def validate_phone_number(value):
        if not value.startswith('5'):
            raise ValidationError("Phone number must start with '5'.")
        
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=8, default='00000000', unique=True, validators=[validate_phone_number], error_messages={'unique':"This phone number is already used."})
    solde = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
    

    
class orange_transaction(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    user_phone_number=models.CharField(max_length=8, default='00000000')
    solde = models.IntegerField(default=0)
    ammount = models.IntegerField(default=0)
    recipient = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.user)
    

