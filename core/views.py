# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard(request):
    from catalog.models import Product, Category
    from stock.models import StockMovement, Stock
    from transfers.models import Transfer
    from suppliers.models import Supplier
    from offices.models import Office
    from purchasing.models import PurchaseOrder

    # إحصاءات
    total_products  = Product.objects.filter(active=True).count()
    total_suppliers = Supplier.objects.filter(active=True).count()
    total_offices   = Office.objects.filter(active=True).count()
    pending_transfers = Transfer.objects.filter(status='pending').count()
    approved_transfers= Transfer.objects.filter(status='approved').count()
    pending_po        = PurchaseOrder.objects.filter(status__in=['pending','approved']).count()

    # تنبيهات المخزون
    low_stock = []
    for s in Stock.objects.select_related('product').all():
        if s.quantity <= s.product.min_stock:
            low_stock.append(s)

    # آخر الحركات
    last_movements = StockMovement.objects.select_related('product').order_by('-date')[:8]

    # آخر السندات
    last_transfers = Transfer.objects.select_related('requested_by').order_by('-created_at')[:6]

    # إحصاء بالفئة
    cat_stats = Category.objects.annotate(
        prod_count=Count('product', filter=Q(product__active=True))
    ).values('name','prod_count')[:8]

    # حركات الأسبوع
    week_ago = timezone.now() - timedelta(days=7)
    week_in  = StockMovement.objects.filter(direction='in',  date__gte=week_ago).count()
    week_out = StockMovement.objects.filter(direction='out', date__gte=week_ago).count()

    ctx = {
        'total_products':   total_products,
        'total_suppliers':  total_suppliers,
        'total_offices':    total_offices,
        'pending_transfers':pending_transfers,
        'approved_transfers':approved_transfers,
        'pending_po':       pending_po,
        'low_stock':        low_stock,
        'last_movements':   last_movements,
        'last_transfers':   last_transfers,
        'cat_stats':        list(cat_stats),
        'week_in':          week_in,
        'week_out':         week_out,
        'out_of_stock':     sum(1 for s in low_stock if s.quantity == 0),
    }
    return render(request, 'core/dashboard.html', ctx)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        password = request.POST.get('password','')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
