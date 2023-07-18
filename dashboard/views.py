from django.shortcuts import render, redirect
from django.http import HttpResponse
from income.models import Income
from expenses.models import Expenses
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from datetime import date
from dashboard.models import Categories
import csv
import io
import datetime
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives

#classes
class UpdatePageForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    amount = forms.IntegerField(label="Amount")
    date = forms.DateField(label="Date",initial=date.today())
    description = forms.CharField(label="Description", max_length=100, required=False,)
    category = forms.ModelChoiceField(queryset=Categories.objects.all())

# Create your views here.

@login_required(login_url="loginpage")
def index(request):
    return render(request,'base.html',{
        'username': request.user.username
    })

@login_required(login_url="loginpage")
def transactions(request):
    userid = request.user.id
    username = request.user.username
    expenses = Expenses.objects.filter(User = userid)
    income = Income.objects.filter(User = userid)
    data = list(expenses) + list(income)
    data.sort(key=lambda x: x.Date, reverse=True)
    return render(request,'transactions.html',{
        'username': username,
        'data': data
    })

def updatePage(request):
    if request.method == 'POST':
        type = request.POST.get("type")
        id = request.POST.get("id")
        username = request.user.username
        if type == "income" :
            data = Income.objects.get(id = id)
            amount = data.Amount
        else : 
            data = Expenses.objects.get(id = id)
            amount = data.Amount*-1
        
        form = UpdatePageForm(initial={
            'name': data.Name,
            'amount': amount,
            'date': data.Date,
            'description': data.Description,
            'category': data.Category,
        })
        return render(request, "update.html", {
            "username" : username,
            "form" : form,
            "type" : type,
            "id" : id
        })

def update(request):
    if request.method == 'POST':
        type = request.POST.get("type")
        id = request.POST.get("id")
        form = UpdatePageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            amount = form.cleaned_data["amount"]
            date = form.cleaned_data["date"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]

            if type == "income" :
                data = Income.objects.get(id = id)
                data.Amount = amount
            else : 
                data = Expenses.objects.get(id = id)
                data.Amount = amount*-1     

            data.Name = name
            data.Date = date 
            data.Description = description
            data.Category = category

            data.save()
            if type == 'income' : 
                return redirect('income')
            else : 
                return redirect('expenses')

def deletePage(request):
    if request.method == "POST":
        type = request.POST.get("type")
        id = request.POST.get("id")
        username = request.user.username

        return render(request, "delete.html", {
            "username" : username,
            "type" : type,
            "id" : id
        }) 
    
def delete(request):
    if request.method == "POST": 
        type = request.POST.get("type")
        id = request.POST.get("id")

        if type == "income":
            data = Income.objects.get(id = id)
        else : 
            data = Expenses.objects.get(id = id)

        data.delete()
        if type == 'income' : 
            return redirect('income')
        else : 
            return redirect('expenses')

def export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expensez' + str(datetime.datetime.now()) + '.csv'
    writer=csv.writer(response)
    writer.writerow(['Name','Amount','Date','Description','Category'])

    userid = request.user.id
    expenses = Expenses.objects.filter(User = userid)
    income = Income.objects.filter(User = userid)
    data = list(expenses) + list(income)
    
    for item in data:
        writer.writerow([item.Name,item.Amount,item.Date,item.Description,item.Category])

    filename = 'Expensez' + str(datetime.datetime.now()) + '.csv'
    name = request.user.username
    mailid = request.user.email
    email_body = "Dear " + name + """ 
Please find attached the CSV file containing the Expensez Stetement.
Thank you for being a valuable customer.

Team Expensez
    """
    email = EmailMessage(
        subject="Expensez Statement",
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[mailid]
    )
    email.attach(filename, response.getvalue(), 'text/csv')
    email.send()
    return response
