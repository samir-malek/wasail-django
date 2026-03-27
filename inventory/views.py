from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InventorySession, InventoryItem
from catalog.models import Product, Category
from stock.models import Stock

@login_required
def inventory_list(request):
    sessions = InventorySession.objects.select_related('conducted_by').all()
    return render(request,'inventory/list.html',{'sessions':sessions})

@login_required
def inventory_new(request):
    cats     = Category.objects.filter(active=True)
    cat_id   = request.GET.get('cat','')
    products = Product.objects.filter(active=True).select_related('unit','category')
    if cat_id: products = products.filter(category_id=cat_id)
    stocks   = {s.product_id: s.quantity for s in Stock.objects.all()}
    if request.method == 'POST':
        session = InventorySession.objects.create(
            conducted_by=request.user,
            scope=request.POST.get('scope','جرد شامل'),
            notes=request.POST.get('notes',''),
            validated_by=request.POST.get('validated_by',''),
        )
        for pid,actual in zip(request.POST.getlist('product_id'),request.POST.getlist('actual')):
            try:
                a=float(actual)
                t=float(stocks.get(int(pid),0))
                InventoryItem.objects.create(
                    session=session,product_id=pid,
                    theoretical_qty=t,actual_qty=a,difference=a-t,
                )
            except: pass
        messages.success(request,f'✅ تم حفظ الجرد | {session.number}')
        return redirect('inventory:detail', pk=session.pk)
    items = [{'p':p,'theo':stocks.get(p.pk,0)} for p in products]
    return render(request,'inventory/new.html',{'items':items,'cats':cats,'cat_id':cat_id})

@login_required
def inventory_detail(request, pk):
    session = get_object_or_404(InventorySession, pk=pk)
    items   = session.items.select_related('product__unit').all()
    summary = session.summary()
    return render(request,'inventory/detail.html',{'session':session,'items':items,'summary':summary})
