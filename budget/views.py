from django.shortcuts import render,redirect,get_object_or_404
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

        passing_dict = {
            "incomes":incomes,
            "expenses":expenses,
            "curr_bal":curr_bal,
            "this_m_spending":this_m_spending
                       
        }
        # if request.method == 'POST':
        #     if 'save' in request.POST:
        #         pk = request.POST.get('save')
        #         if not pk:
        #             form = ExpenseForm(request.POST)
        #         else:
        #             record = Expense.objects.get(id=pk)
        #             form = ExpenseForm(request.POST,instance=record)
        #         form.save()
        #         return redirect(reverse('index'))
                
        #     if 'save_Income' in request.POST:
        #         pk = request.POST.get('save_Income')
        #         if not pk:
        #             form_income = IncomeForm(request.POST)
        #         else:
        #             record = Income.objects.get(id=pk)
        #             form_income = IncomeForm(request.POST,instance=record)
        #         form_income.save()
        #         return redirect(reverse('index'))
            
        #     if 'delete' in request.POST:
        #         pk = request.POST.get('delete')
        #         record = Expense.objects.get(id=pk)
        #         record.delete()
                
        #     if 'delete_income' in request.POST:
        #         pk = request.POST.get('delete_income')
        #         record = Income.objects.get(id=pk)
        #         record.delete()
                
        #     if 'edit_income' in request.POST:
        #         pk = request.POST.get('edit_income')
        #         record = Income.objects.get(id=pk)
        #         form_income = IncomeForm(instance=record)
                
        #     if 'edit_expense' in request.POST:
        #         pk = request.POST.get('edit_expense')
        #         record = Expense.objects.get(id=pk)
        #         form = ExpenseForm(instance=record)

        # passing_dict['form'] = form
        # passing_dict['form_income'] = form_income
            
        
                
    except Exception as e:
        raise (f"Ran into an exception")
    return render(request, "budget/index.html", passing_dict)


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        # Checing if form is valid and checks all the validations
        if form.is_valid():
            
            form.save()
            return redirect('index')
    else:
        form = ExpenseForm()
    # Returning an empty form after recieving an invalid form
    return render(request, "budget/expense_form.html",{'form':form})


def add_income(request):
    if request.method == 'POST':
        form_income = IncomeForm(request.POST)
        if form_income.is_valid():

            form_income.save()
            return redirect('index')
        
    else:
        form_income = IncomeForm()
            
    return render(request, "budget/income_form.html",{'form_income':form_income})

def edit_income(request, edit_id):
    record = get_object_or_404(Income,id = edit_id)
    if request.method == 'POST':
        form_income = IncomeForm(request.POST, instance=record)
        if form_income.is_valid():
            form_income.save()
            return redirect('index')
    else:
        form_income = IncomeForm(instance=record)
    return render(request, "budget/income_form.html",{'form_income':form_income})    


def edit_expense(request,edit_id):
    record = get_object_or_404(Expense,id=edit_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('index')
        
    else:
        form = ExpenseForm(instance=record)
    return render(request,"budget/expense_form.html", {'form':form})


def delete_expense(request,delete_id):

    if request.method == 'POST':
        record = get_object_or_404(Expense,id=delete_id)
        record.delete()
    return redirect('index')
    
    
def delete_income(request, delete_id):
    if request.method == 'POST':
        record = get_object_or_404(Income,id=delete_id)
        record.delete()
    return redirect('index')


