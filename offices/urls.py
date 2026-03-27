from django.urls import path
from . import views
app_name = 'offices'
urlpatterns = [
    path('', views.office_list, name='list'),
    path('add/', views.office_add, name='add'),
    path('<int:pk>/', views.office_detail, name='detail'),
    path('managers/', views.managers, name='managers'),
    path('managers/assign/', views.assign_manager, name='assign_manager'),
]
