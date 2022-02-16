from django.urls import path,include
from tutorial.views import *
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView

app_name='tutorial'
urlpatterns = [
    path('',index,name='index'),
    path('tutorial/',tutorial,name='tutorial'),
    path('detail/<int:pk>/',detail,name='detail'),

    path('loginpage/',loginpage,name='loginpage'),
    path('register/',register,name='register'),
    path('logout/',logout_request,name='logout_request'),
    path('profile/',profile,name='profile'),

    path("password-reset/done/", PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="tutorial/password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name='tutorial/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/", PasswordResetCompleteView.as_view(template_name='tutorial/password_reset_complete.html'), name="password_reset_complete"),
    path("password-reset/", PasswordResetView.as_view(template_name='tutorial/password_reset.html'), name="password_reset"),

    path('ajax/like/',like,name='like'),
    path('reply/',reply,name='reply'),
    path('comment/',comment,name='comment'),

    path('login_faculty/',login_faculty,name='login_faculty'),

]