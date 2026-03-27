from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.dashboard, name='dashboard'),
    path('login/', core_views.login_view, name='login'),
    path('logout/', core_views.logout_view, name='logout'),
    path('catalog/', include('catalog.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('offices/', include('offices.urls')),
    path('stock/', include('stock.urls')),
    path('transfers/', include('transfers.urls')),
    path('purchasing/', include('purchasing.urls')),
    path('inventory/', include('inventory.urls')),
    path('reports/', include('reports.urls')),
]
