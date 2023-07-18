from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('transactions',views.transactions,name='transactions'),
    path('updatePage',views.updatePage,name='updatePage'),
    path('update',views.update,name='update'),
    path('delete', views.delete, name="delete"),
    path('deletePage', views.deletePage, name="deletePage"),
    path('export',views.export, name='export'),
]
