from django.urls import path
from . import views

urlpatterns =[
    path('', views.log_in, name="login"),
    path('ft_login', views.ft_log_in, name="ft_login"),
]