from django import forms
from .models import Expense,Income

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category_name','expense_note', 'amount']
        

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['bank','amount']