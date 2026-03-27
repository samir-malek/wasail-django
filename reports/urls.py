from django.urls import path
from . import views
app_name = 'reports'
urlpatterns = [
    path('', views.index, name='index'),
    path('stock/', views.stock_report, name='stock'),
    path('movements/', views.movements_report, name='movements'),
    path('transfers/', views.transfers_report, name='transfers'),
]
