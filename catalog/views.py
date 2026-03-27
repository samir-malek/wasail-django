from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Unit
from stock.models import Stock

@login_required
def products(request):
    qs = Product.objects.filter(active=True).select_related('category','unit')
    search   = request.GET.get('q','')
    cat_id   = request.GET.get('cat','')
    stock_f  = request.GET.get('stock','')
    if search:  qs = qs.filter(Q(name__icontains=search)|Q(code__icontains=search))
    if cat_id:  qs = qs.filter(category_id=cat_id)
    cats = Category.objects.filter(active=True)
    # تحضير حالة المخزون
    prods = []
    for p in qs:
        status, color = p.stock_status()
        if stock_f and stock_f != color: continue
        prods.append({'obj':p,'qty':p.current_stock(),'status':status,'color':color})
    return render(request,'catalog/products.html',{'prods':prods,'cats':cats,'search':search,'cat_id':cat_id})

@login_required
def product_add(request):
    cats  = Category.objects.filter(active=True)
    units = Unit.objects.filter(active=True)
    if request.method == 'POST':
        try:
            p = Product(
                code=request.POST['code'].upper().strip(),
                name=request.POST['name'].strip(),
                name_fr=request.POST.get('name_fr','').strip(),
                category_id=request.POST['category'],
                unit_id=request.POST['unit'],
                min_stock=request.POST.get('min_stock',5),
                max_stock=request.POST.get('max_stock',100),
                reorder_qty=request.POST.get('reorder_qty',20),
                brand=request.POST.get('brand','').strip(),
                model=request.POST.get('model','').strip(),
                description=request.POST.get('description','').strip(),
                specifications=request.POST.get('specifications','').strip(),
                created_by=request.user,
            )
            p.save()
            Stock.objects.get_or_create(product=p, defaults={'quantity':0})
            messages.success(request, f'✅ تمت إضافة المنتج: {p.name}')
            return redirect('catalog:products')
        except Exception as e:
            messages.error(request, f'❌ {e}')
    return render(request,'catalog/product_form.html',{'cats':cats,'units':units,'action':'add'})

@login_required
def product_edit(request, pk):
    p     = get_object_or_404(Product, pk=pk)
    cats  = Category.objects.filter(active=True)
    units = Unit.objects.filter(active=True)
    if request.method == 'POST':
        p.name=request.POST['name'].strip()
        p.name_fr=request.POST.get('name_fr','').strip()
        p.category_id=request.POST['category']
        p.unit_id=request.POST['unit']
        p.min_stock=request.POST.get('min_stock',5)
        p.max_stock=request.POST.get('max_stock',100)
        p.brand=request.POST.get('brand','').strip()
        p.description=request.POST.get('description','').strip()
        p.active = 'active' in request.POST
        p.save()
        messages.success(request, '✅ تم حفظ التعديلات')
        return redirect('catalog:products')
    return render(request,'catalog/product_form.html',{'p':p,'cats':cats,'units':units,'action':'edit'})

@login_required
def categories(request):
    if request.method == 'POST':
        Category.objects.create(
            name=request.POST['name'].strip(),
            name_fr=request.POST.get('name_fr','').strip(),
            icon=request.POST.get('icon','📦'),
            description=request.POST.get('description','').strip(),
        )
        messages.success(request, '✅ تمت إضافة الفئة')
        return redirect('catalog:categories')
    cats = Category.objects.annotate_product_count() if hasattr(Category.objects,'annotate_product_count') else Category.objects.all()
    from django.db.models import Count
    cats = Category.objects.filter(active=True).annotate(cnt=Count('product'))
    return render(request,'catalog/categories.html',{'cats':cats})

@login_required
def units(request):
    if request.method == 'POST':
        Unit.objects.create(
            name=request.POST['name'].strip(),
            name_fr=request.POST.get('name_fr','').strip(),
            symbol=request.POST['symbol'].strip(),
        )
        messages.success(request, '✅ تمت إضافة الوحدة')
        return redirect('catalog:units')
    units = Unit.objects.filter(active=True)
    return render(request,'catalog/units.html',{'units':units})
