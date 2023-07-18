from django.urls import path
from . import views

urlpatterns = [
    path('income',views.income,name='income'),
    # path('transactions',views.transactions,name='transactions'),
    path('addIncome',views.addIncome,name='addIncome'),
    # path('delete',views.delete,name='delete'),
]
