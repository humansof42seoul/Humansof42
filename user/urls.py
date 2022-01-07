from django.urls import path
from . import views

urlpatterns =[
    path('mypage/', views.get_mypage, name="mypage"),
    path('change_email/', views.change_email, name="change_email"),
    path('change_password/', views.change_password, name="change_password")
]