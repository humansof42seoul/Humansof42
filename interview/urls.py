from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('<int:pk>', views.interview_detail, name="interview_detail"),
    path('write/', views.interview_write, name="interview_write"),
    path('<int:pk>/edit', views.interview_edit, name="interview_edit"),
    path('like/', views.like_interview, name="like_interview"),
    path('<int:pk>/comment/write', views.write_comment, name='write_comment'),
    path('<int:pk>/comment/delete', views.delete_comment, name='delete_comment'),
    path('', views.interview_list),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]