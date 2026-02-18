# budget/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path("expense/delete/<int:delete_id>/", views.delete_expense, name="delete_expense"),
    path("income/delete/<int:delete_id>/", views.delete_income, name="delete_income"),
    
    path("expense/add/", views.add_expense, name="add_expense"),
    path("income/add/", views.add_income, name="add_income"),
    
    path("expense/edit/<int:edit_id>/", views.edit_expense, name="edit_expense"),
    path("income/edit/<int:edit_id>/", views.edit_income, name="edit_income"),
    
]
