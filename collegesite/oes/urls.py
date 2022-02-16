from django.urls import path,include
from oes.views import *

app_name='oes'
urlpatterns = [
    path('',index,name='index'),
    path('examinations/',examinations,name='examinations'),
    path('result_analysis/',result_analysis,name='result_analysis'),
    path('user_registration/',user_registration,name='user_registration'),
    path('approved_exams/',approved_exams,name='approved_exams'),
    path('approved_exams/instructions/<int:pk>',instructions,name='instructions'),
    path('approved_exams/instructions/questions/<int:pk>/<int:pk1>',questions,name='questions'),
    path('approved_exams/instructions/questions/res',res,name='res'),
    path('approved_exams/instructions/questions/result/<int:pk>/<int:pk1>',result,name='result'),

    path('faculty_dashboard/',faculty_dashboard,name='faculty_dashboard'),
    path('progress/',progress,name='progress'),
    path('fac_exam_registration/',fac_exam_registration,name='fac_exam_registration'),
    path('fac_examinations/',fac_examinations,name='fac_examinations'),
    path('create/',Ex_view.as_view(),name='create'),
    path('update/<int:pk>',Ex_update_view.as_view(),name='update'),
    path('delete/<int:pk>',Ex_delete_view.as_view(),name='delete'),
    path('fac_logout/',fac_logout,name='fac_logout'),
]