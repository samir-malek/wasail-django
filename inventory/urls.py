from django.urls import path
from . import views
app_name = 'inventory'
urlpatterns = [
    path('', views.inventory_list, name='list'),
    path('new/', views.inventory_new, name='new'),
    path('<int:pk>/', views.inventory_detail, name='detail'),
]
