from django.urls import path
from . import views
app_name = 'transfers'
urlpatterns = [
    path('', views.transfer_list, name='list'),
    path('new/', views.transfer_new, name='new'),
    path('<int:pk>/', views.transfer_detail, name='detail'),
    path('<int:pk>/approve/', views.transfer_approve, name='approve'),
    path('<int:pk>/reject/', views.transfer_reject, name='reject'),
    path('<int:pk>/execute/', views.transfer_execute, name='execute'),
    path('<int:pk>/receive/', views.transfer_receive, name='receive'),
    path('<int:pk>/print/', views.transfer_print, name='print'),
]
