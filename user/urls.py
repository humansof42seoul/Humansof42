from django.urls import path
from . import views

urlpatterns =[
    path('mypage/', views.get_mypage, name="mypage"),
]