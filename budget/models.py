from django.db import models
from django.utils import timezone
import datetime
# Create your models here.


class Income(models.Model):
    BANK_NAME_CHOICES = [
        ("BOI","Bank of India"),
        ("ICI","ICICI Bank"),
    ]
    bank = models.CharField(choices=BANK_NAME_CHOICES,max_length=3)
    amount = models.DecimalField(blank=False,null=False,max_digits=7,decimal_places=2)
    recieve_date = models.DateTimeField(auto_now=True)
    
class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ("W","Wants"),
        ("N","Needs"),
        ("I","Investments"),
        ("E","Emergency"),
    ]
    c_name = models.CharField(max_length=15,null=False, blank=False)
    c_type = models.CharField(choices=CATEGORY_TYPE_CHOICES,max_length=1)
    
    def __str__(self):
        return f"{self.c_name} ({self.get_c_type_display()})"
    

class Expense(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    expense_note = models.CharField(max_length=100,blank=False,null=False)
    amount = models.DecimalField(blank=False,null=False, max_digits=7,decimal_places=2)
    spend_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.expense_note} "
    



