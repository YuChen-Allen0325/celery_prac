from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.AddView.as_view(), name='task'),
    path('cache/', views.MyDataView.as_view(), name='cache'),
]
