from django.db import models

# Create your models here.

class unicom_transaction(models.Model):

    SERVICE_PROVIDER_OPTIONS = [
        ('ooredoo', 'ooredoo'),
        ('orange', 'orange'),
        ('telecom', 'telecom')]
    

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    user_phone_number=models.CharField(max_length=8, default='00000000')

    user_service_provider=models.CharField(choices=SERVICE_PROVIDER_OPTIONS ,max_length=8, default='unicom')
    solde = models.IntegerField(default=0)
    ammount = models.IntegerField(default=0)
    recipient = models.CharField(max_length=8)
    recipient_service_provider=models.CharField(choices=SERVICE_PROVIDER_OPTIONS ,max_length=8, default='unicom')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.user)