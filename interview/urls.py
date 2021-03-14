from django.urls import path
from . import views

urlpatterns =[
    path('<int:pk>', views.interview_detail, name="interview_detail"),
    path('write/', views.interview_write, name="interview_write"),
    path('<int:pk>/edit', views.interview_edit, name="interview_edit"),
    path('like/', views.like_interview, name="like_interview"),
    path('<int:pk>/comment/write', views.write_comment, name='write_comment'),
    path('<int:pk>/comment/delete', views.delete_comment, name='delete_comment'),
    path('', views.interview_list),
]