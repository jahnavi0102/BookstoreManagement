from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    """
    Users/Customers data to be stored in this mode. 
    This model is used for authentication purpose.
    """

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
       return self.email


    



    




