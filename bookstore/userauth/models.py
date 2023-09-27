from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    """
    Users/Customers data to be stored in this mode. 
    This model is used for authentication purpose.
    """
    def __str__(self):
       return self.email


    



    




