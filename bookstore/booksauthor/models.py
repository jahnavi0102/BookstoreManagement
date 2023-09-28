from django.db import models

class Authors():
    """
    Authors data to be stored in this model. 
    """
    name = models.CharField(max_length=200,blank=False)
    def __str__(self):
       return self.name
    
class Books():
    """
    Books data to be stored in this model. 
    """
    title = models.CharField(max_length=300, blank=False)
    isbn = models.CharField(max_length=100, blank=False, primary_key=True)
    price = models.FloatField(blank=False)
    quantity = models.IntegerField(blank=False, default=1)
    written_by = models.ManyToManyField(Authors)
    def __str__(self):
       return self.title
    


    



