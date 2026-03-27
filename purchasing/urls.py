from django.urls import path
from . import views
app_name = 'purchasing'
urlpatterns = [
    path('', views.po_list, name='list'),
    path('receive/', views.receive_goods, name='receive'),
    path('po/new/', views.po_new, name='po_new'),
    path('po/<int:pk>/approve/', views.po_approve, name='po_approve'),
    path('invoices/', views.invoice_list, name='invoices'),
]
