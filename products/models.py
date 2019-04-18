from django.db import models

# Create your models here.
class Product(models.Model):
    """what will create on db for that product. Specify columns that will be within tables on db"""
    name = models.CharField(max_length=254, default='') # by default is empty, we won't add any default product on db
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2) #anything under a million
    image = models.ImageField(upload_to='images') # upload to a directory called images
    
    def __str__(self):
        return self.name
    