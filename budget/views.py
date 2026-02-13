from django.shortcuts import render,redirect
from .models import Income, Expense
from .forms import ExpenseForm,IncomeForm
from django.utils import timezone
from django.urls import reverse

from django.db.models import Sum

# Create your views here.

def current_balance():
    total_inc = Income.objects.aggregate(income = Sum('amount'))['income'] or 0
    total_exp = Expense.objects.aggregate(expense = Sum('amount'))['expense'] or 0
    return total_inc - total_exp

def list_of_incomes():
    incomes = Income.objects.all().order_by('-id')
    return incomes


def list_of_expences():
    expences = Expense.objects.all().order_by('-id')
    return expences
    

def this_month_spending():
    now = timezone.now()
    total = (
        Expense.objects
        .filter(
            spend_date__year=now.year,
            spend_date__month=now.month,
        )
        .aggregate(total=Sum("amount"))    
        )
    return total['total'] or 0


def category_comparision():
    now = timezone.now()
    qs = (
    Expense.objects
    .filter(
        spend_date__year=now.year,
        spend_date__month=now.month,
    )
    .values("category_name")
    .annotate(total_amount=Sum("amount")))
    
    return qs['total_amount']

def index(request):
    try:
        
        incomes = list_of_incomes()
        expenses = list_of_expences()
        curr_bal = current_balance()
        this_m_spending = this_month_spending()
        form = ExpenseForm()
        form_income = IncomeForm()
        passing_dict = {
            "incomes":incomes,
            "expenses":expenses,
            "curr_bal":curr_bal,
            "this_m_spending":this_m_spending,
            "form":form,
            "form_income":form_income
           
            # "catg_comp":catg_comp
            
        }
        if request.method == 'POST':
            if 'save' in request.POST:
                pk = request.POST.get('save')
                if not pk:
                    form = ExpenseForm(request.POST)
                else:
                    record = Expense.objects.get(id=pk)
                    form = ExpenseForm(request.POST,instance=record)
                form.save()
                return redirect(reverse('index'))
                
            if 'save_Income' in request.POST:
                pk = request.POST.get('save_Income')
                if not pk:
                    form_income = IncomeForm(request.POST)
                else:
                    record = Income.objects.get(id=pk)
                    form_income = IncomeForm(request.POST,instance=record)
                form_income.save()
                return redirect(reverse('index'))
            
            if 'delete' in request.POST:
                pk = request.POST.get('delete')
                record = Expense.objects.get(id=pk)
                record.delete()
                
            if 'delete_income' in request.POST:
                pk = request.POST.get('delete_income')
                record = Income.objects.get(id=pk)
                record.delete()
                
            if 'edit_income' in request.POST:
                pk = request.POST.get('edit_income')
                record = Income.objects.get(id=pk)
                form_income = IncomeForm(instance=record)
                # return redirect(reverse('index'))
                
            if 'edit_expense' in request.POST:
                pk = request.POST.get('edit_expense')
                record = Expense.objects.get(id=pk)
                form = ExpenseForm(instance=record)
                # return redirect(reverse('index'))
                
                
        # passing_dict['incomes'] = incomes
        # passing_dict['expenses'] = expenses
        passing_dict['form'] = form
        passing_dict['form_income'] = form_income
            
        
                
    except Exception as e:
        raise (f"Ran into an exception")
    return render(request, "budget/index.html", passing_dict)


