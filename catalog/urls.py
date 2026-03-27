from django.urls import path
from . import views
app_name = 'catalog'
urlpatterns = [
    path('', views.products, name='products'),
    path('add/', views.product_add, name='product_add'),
    path('<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('categories/', views.categories, name='categories'),
    path('units/', views.units, name='units'),
]
