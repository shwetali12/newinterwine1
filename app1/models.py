from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class OfferType(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Offer(models.Model):

    mytype = models.ForeignKey(OfferType, on_delete=models.CASCADE)
    amount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mytype} - {self.mytype.name}"
    



   