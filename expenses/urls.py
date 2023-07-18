from django.urls import path
from . import views

urlpatterns = [
    path('expenses',views.expenses,name='expenses'),
    # path('transactions',views.transactions,name='transactions'),
    path('addExpense',views.addExpense,name='addExpense'),
    # path('delete',views.delete,name='delete'),
]
