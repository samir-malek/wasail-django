from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Stock, StockMovement
from catalog.models import Product

@login_required
def stock_list(request):
    stocks = Stock.objects.select_related('product','product__category','product__unit').all()
    filt   = request.GET.get('f','')
    items  = []
    for s in stocks:
        status, color = s.product.stock_status()
        if filt == 'low'  and color not in ('danger','warning'): continue
        if filt == 'zero' and color != 'danger': continue
        items.append({'s':s,'status':status,'color':color})
    out_of = sum(1 for i in items if i['color']=='danger')
    low    = sum(1 for i in items if i['color']=='warning')
    return render(request,'stock/list.html',{'items':items,'filt':filt,'out_of':out_of,'low':low})

@login_required
def movements(request):
    qs = StockMovement.objects.select_related('product','created_by').all()
    q  = request.GET.get('q','')
    d  = request.GET.get('dir','')
    if q: qs = qs.filter(Q(product__name__icontains=q)|Q(reference_number__icontains=q))
    if d: qs = qs.filter(direction=d)
    return render(request,'stock/movements.html',{'movements':qs[:200],'q':q,'d':d})
