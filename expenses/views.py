from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Expenses
from dashboard.models import Categories
from django import forms
from django.contrib import messages
from datetime import date


# Classes
class AddExpenseForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    amount = forms.IntegerField(label="Amount")
    date = forms.DateField(label="Date",initial=date.today())
    description = forms.CharField(label="Description", max_length=100, required=False, )
    category = forms.ModelChoiceField(queryset=Categories.objects.all())

# Create your views here.

@login_required(login_url="loginpage")
def expenses(request):
    userid = request.user.id
    username = request.user.username
    expenses = Expenses.objects.filter(User = userid)
    data = list(expenses)
    data.sort(key=lambda x: x.Date, reverse=True)
    return render(request,'transactions.html',{
        'username': username,
        'data': data
    })

@login_required
def addExpense(request):
    if request.method == "POST":
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            amount = form.cleaned_data["amount"]
            amount *= -1
            date = form.cleaned_data["date"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            user = request.user

            expense = Expenses.objects.create(
                User = user,
                Name = name,
                Amount = amount,
                Date = date,
                Description = description,
                Category = category
            )
            expense.save()
            print("add expense")
            return redirect('expenses')
    else:   
        form =  AddExpenseForm()
    
    username = request.user.username
    return render(request, "add.html", {
        "data" : "Expense",
        "username" : username,
        "form" : AddExpenseForm()
    })
