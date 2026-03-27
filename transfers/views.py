from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Transfer, TransferItem
from catalog.models import Product
from offices.models import Office
from stock.models import Stock, StockMovement

@login_required
def transfer_list(request):
    role = request.user.profile.role
    qs   = Transfer.objects.select_related('requested_by','requesting_office').all()
    if role == 'chef':
        qs = qs.filter(requesting_dept=request.user.profile.department)
    status = request.GET.get('status','')
    if status: qs = qs.filter(status=status)
    pending_count = Transfer.objects.filter(status='pending').count()
    return render(request,'transfers/list.html',{'transfers':qs,'pending_count':pending_count,'status':status})

@login_required
def transfer_new(request):
    products = Product.objects.filter(active=True).select_related('unit')
    offices  = Office.objects.filter(active=True)
    if request.method == 'POST':
        dept = request.POST.get('dept', request.user.profile.department)
        t = Transfer(
            requesting_dept=dept,
            requested_by=request.user,
            transfer_type=request.POST.get('transfer_type','normal'),
            priority=request.POST.get('priority','normal'),
            notes=request.POST.get('notes',''),
        )
        off_id = request.POST.get('office')
        if off_id:
            t.requesting_office_id = off_id
        t.save()
        # حفظ المواد
        ids   = request.POST.getlist('product_id')
        qtys  = request.POST.getlist('qty')
        saved = 0
        for pid, qty in zip(ids, qtys):
            try:
                qty_f = float(qty)
                if qty_f > 0 and pid:
                    TransferItem.objects.create(transfer=t, product_id=pid, requested_qty=qty_f)
                    saved += 1
            except: pass
        if saved == 0:
            t.delete()
            messages.error(request,'❌ أضف مادة واحدة على الأقل')
        else:
            messages.success(request, f'✅ تم إرسال الطلب | رقم: {t.number}')
            return redirect('transfers:list')
    stocks = {s.product_id: s.quantity for s in Stock.objects.all()}
    return render(request,'transfers/new.html',{'products':products,'offices':offices,'stocks':stocks})

@login_required
def transfer_detail(request, pk):
    t = get_object_or_404(Transfer, pk=pk)
    return render(request,'transfers/detail.html',{'t':t,'items':t.items.select_related('product__unit')})

@login_required
def transfer_approve(request, pk):
    t = get_object_or_404(Transfer, pk=pk)
    if request.method == 'POST':
        t.status='approved'; t.approved_by=request.user; t.approved_at=timezone.now(); t.save()
        messages.success(request, f'✅ تمت الموافقة على {t.number}')
    return redirect('transfers:list')

@login_required
def transfer_reject(request, pk):
    t = get_object_or_404(Transfer, pk=pk)
    if request.method == 'POST':
        t.status='rejected'; t.approved_by=request.user; t.approved_at=timezone.now()
        t.rejection_reason=request.POST.get('reason',''); t.save()
        messages.warning(request, f'❌ تم رفض {t.number}')
    return redirect('transfers:list')

@login_required
def transfer_execute(request, pk):
    t = get_object_or_404(Transfer, pk=pk)
    if request.method == 'POST':
        for item in t.items.all():
            key = f'delivered_{item.pk}'
            try:
                dqty = float(request.POST.get(key, 0))
                if dqty > 0:
                    item.delivered_qty = dqty; item.save()
                    # خصم المخزون
                    stock, _ = Stock.objects.get_or_create(product=item.product, defaults={'quantity':0})
                    stock.quantity = max(0, stock.quantity - dqty); stock.save()
                    StockMovement.objects.create(
                        direction='out', product=item.product, quantity=dqty,
                        reference_type='transfer', reference_number=t.number,
                        from_location='المخزن الرئيسي', to_location=t.requesting_dept,
                        created_by=request.user,
                    )
            except: pass
        t.status='executed'; t.executed_by=request.user; t.executed_at=timezone.now(); t.save()
        messages.success(request, f'✅ تم تنفيذ {t.number}')
    return redirect('transfers:list')

@login_required
def transfer_receive(request, pk):
    t = get_object_or_404(Transfer, pk=pk)
    if request.method == 'POST':
        t.status='received'; t.received_by=request.user; t.received_at=timezone.now(); t.save()
        messages.success(request, f'✅ تم تأكيد الاستلام — {t.number}')
    return redirect('transfers:list')

@login_required
def transfer_print(request, pk):
    t = get_object_or_404(Transfer, pk=pk)
    return render(request,'transfers/print.html',{'t':t,'items':t.items.select_related('product__unit')})
