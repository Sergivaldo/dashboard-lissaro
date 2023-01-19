from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Keys(models.Model):
    public_key = models.TextField()
    private_key = models.TextField()


class ApiData(models.Model):
    bank_accounts = models.TextField()
    payments = models.TextField()
    receivements = models.TextField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f'ApiData {self.pk}'


class BlingUser(models.Model):
    user_name = models.CharField(max_length=65, null=True)
    password = models.CharField(max_length=255, null=True)
    api_key = models.CharField(max_length=255, null=True)
    dashboard_user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)
    api_data = models.OneToOneField(
        ApiData, on_delete=models.CASCADE, null=True, blank=True)
    keys = models.OneToOneField(Keys, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user_name}({self.pk})'
