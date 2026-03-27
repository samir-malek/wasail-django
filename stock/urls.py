from django.urls import path
from . import views
app_name = 'stock'
urlpatterns = [
    path('', views.stock_list, name='list'),
    path('movements/', views.movements, name='movements'),
]
