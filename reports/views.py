from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stock.models import Stock, StockMovement
from transfers.models import Transfer
from catalog.models import Product, Category
from suppliers.models import Supplier
from django.db.models import Count, Sum, Q

@login_required
def index(request):
    return render(request,'reports/index.html')

@login_required
def stock_report(request):
    stocks = Stock.objects.select_related('product__category','product__unit').all()
    items=[]
    for s in stocks:
        status,color=s.product.stock_status()
        items.append({'s':s,'status':status,'color':color})
    total=len(items); zero=sum(1 for i in items if i['color']=='danger')
    low=sum(1 for i in items if i['color']=='warning')
    ok=sum(1 for i in items if i['color']=='success')
    return render(request,'reports/stock.html',{'items':items,'total':total,'zero':zero,'low':low,'ok':ok})

@login_required
def movements_report(request):
    qs = StockMovement.objects.select_related('product').all()
    d  = request.GET.get('dir','')
    if d: qs=qs.filter(direction=d)
    ins  = qs.filter(direction='in').count()
    outs = qs.filter(direction='out').count()
    return render(request,'reports/movements.html',{'movements':qs[:300],'ins':ins,'outs':outs,'d':d})

@login_required
def transfers_report(request):
    qs = Transfer.objects.all()
    by_status = qs.values('status').annotate(c=Count('id'))
    by_dept   = qs.values('requesting_dept').annotate(c=Count('id')).order_by('-c')[:10]
    return render(request,'reports/transfers.html',{'qs':qs,'by_status':by_status,'by_dept':by_dept})
