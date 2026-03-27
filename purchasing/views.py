from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import PurchaseOrder, PurchaseItem, Invoice, InvoiceItem
from catalog.models import Product
from suppliers.models import Supplier
from stock.models import Stock, StockMovement
import datetime

@login_required
def po_list(request):
    pos = PurchaseOrder.objects.select_related('supplier','requested_by').all()
    return render(request,'purchasing/po_list.html',{'pos':pos})

@login_required
def po_new(request):
    suppliers = Supplier.objects.filter(active=True)
    products  = Product.objects.filter(active=True).select_related('unit')
    if request.method == 'POST':
        sup = get_object_or_404(Supplier, pk=request.POST['supplier'])
        po  = PurchaseOrder.objects.create(
            supplier=sup, requested_by=request.user,
            priority=request.POST.get('priority','عادي'),
            notes=request.POST.get('notes',''),
            expected_delivery=request.POST.get('expected_delivery') or None,
        )
        total = 0
        for pid,qty,price in zip(
            request.POST.getlist('product_id'),
            request.POST.getlist('qty'),
            request.POST.getlist('price'),
        ):
            try:
                q=float(qty); p=float(price) if price else 0
                if q>0 and pid:
                    PurchaseItem.objects.create(order=po,product_id=pid,requested_qty=q,unit_price=p,total_price=q*p)
                    total += q*p
            except: pass
        po.total_amount=total; po.save()
        messages.success(request,f'✅ طلب الشراء: {po.number}')
        return redirect('purchasing:list')
    return render(request,'purchasing/po_form.html',{'suppliers':suppliers,'products':products})

@login_required
def po_approve(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        po.status='approved'; po.approved_by=request.user; po.approved_at=timezone.now(); po.save()
        messages.success(request,f'✅ تم اعتماد {po.number}')
    return redirect('purchasing:list')

@login_required
def receive_goods(request):
    suppliers = Supplier.objects.filter(active=True)
    products  = Product.objects.filter(active=True).select_related('unit')
    if request.method == 'POST':
        sup = get_object_or_404(Supplier, pk=request.POST['supplier'])
        inv = Invoice.objects.create(
            invoice_number=request.POST['invoice_number'].strip(),
            date=request.POST.get('date', str(datetime.date.today())),
            supplier=sup,
            received_by=request.user,
            notes=request.POST.get('notes',''),
        )
        total=0
        for pid,qty,price in zip(
            request.POST.getlist('product_id'),
            request.POST.getlist('qty'),
            request.POST.getlist('price'),
        ):
            try:
                q=float(qty); p=float(price) if price else 0
                if q>0 and pid:
                    prod = Product.objects.get(pk=pid)
                    InvoiceItem.objects.create(invoice=inv,product=prod,quantity=q,unit_price=p,total_price=q*p)
                    stock,_ = Stock.objects.get_or_create(product=prod,defaults={'quantity':0})
                    stock.quantity+=q; stock.save()
                    StockMovement.objects.create(
                        direction='in',product=prod,quantity=q,unit_cost=p,
                        reference_type='invoice',reference_number=inv.number,
                        from_location=sup.name,to_location='المخزن الرئيسي',
                        created_by=request.user,
                    )
                    total+=q*p
            except: pass
        inv.total_amount=total; inv.save()
        messages.success(request,f'✅ تم تسجيل الاستلام | {inv.number}')
        return redirect('purchasing:invoices')
    return render(request,'purchasing/receive.html',{'suppliers':suppliers,'products':products})

@login_required
def invoice_list(request):
    invs = Invoice.objects.select_related('supplier','received_by').all()
    return render(request,'purchasing/invoices.html',{'invs':invs})
