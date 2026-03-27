from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Supplier, SupplierContact

WILAYAS = ["أدرار","الشلف","الأغواط","أم البواقي","باتنة","بجاية","بسكرة","بشار","البليدة","البويرة","تمنراست","تبسة","تلمسان","تيارت","تيزي وزو","الجزائر","الجلفة","جيجل","سطيف","سعيدة","سكيكدة","سيدي بلعباس","عنابة","قالمة","قسنطينة","المدية","مستغانم","المسيلة","معسكر","ورقلة","وهران","البيض","إليزي","برج بوعريريج","بومرداس","الطارف","تندوف","تيسمسيلت","الوادي","خنشلة","سوق أهراس","تيبازة","ميلة","عين الدفلى","النعامة","عين تموشنت","غرداية","غليزان"]

@login_required
def supplier_list(request):
    qs = Supplier.objects.filter(active=True)
    q  = request.GET.get('q','')
    if q: qs = qs.filter(Q(name__icontains=q)|Q(code__icontains=q)|Q(phone__icontains=q))
    return render(request,'suppliers/list.html',{'suppliers':qs,'q':q})

@login_required
def supplier_add(request):
    if request.method == 'POST':
        try:
            s = Supplier(
                code=request.POST['code'].upper().strip(),
                name=request.POST['name'].strip(),
                name_fr=request.POST.get('name_fr','').strip(),
                supplier_type=request.POST.get('supplier_type','private'),
                phone=request.POST.get('phone','').strip(),
                phone2=request.POST.get('phone2','').strip(),
                email=request.POST.get('email','').strip(),
                address=request.POST.get('address','').strip(),
                wilaya=request.POST.get('wilaya',''),
                nif=request.POST.get('nif','').strip(),
                nis=request.POST.get('nis','').strip(),
                rc=request.POST.get('rc','').strip(),
                bank_name=request.POST.get('bank_name','').strip(),
                bank_account=request.POST.get('bank_account','').strip(),
                payment_terms=request.POST.get('payment_terms','cash'),
                delivery_days=request.POST.get('delivery_days',7),
                rating=request.POST.get('rating',3),
                notes=request.POST.get('notes','').strip(),
            )
            s.save()
            messages.success(request, f'✅ تمت إضافة المورد: {s.name}')
            return redirect('suppliers:list')
        except Exception as e:
            messages.error(request, f'❌ {e}')
    return render(request,'suppliers/form.html',{'action':'add','wilayas':WILAYAS})

@login_required
def supplier_detail(request, pk):
    s = get_object_or_404(Supplier, pk=pk)
    contacts = s.contacts.filter(active=True)
    if request.method == 'POST':
        SupplierContact.objects.create(
            supplier=s,
            full_name=request.POST['full_name'].strip(),
            position=request.POST.get('position','').strip(),
            phone=request.POST.get('phone','').strip(),
            email=request.POST.get('email','').strip(),
        )
        messages.success(request,'✅ تمت إضافة جهة الاتصال')
        return redirect('suppliers:detail', pk=pk)
    return render(request,'suppliers/detail.html',{'s':s,'contacts':contacts})

@login_required
def supplier_edit(request, pk):
    s = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        s.name=request.POST['name'].strip()
        s.phone=request.POST.get('phone','').strip()
        s.email=request.POST.get('email','').strip()
        s.rating=request.POST.get('rating',3)
        s.payment_terms=request.POST.get('payment_terms','cash')
        s.notes=request.POST.get('notes','').strip()
        s.active = 'active' in request.POST
        s.save()
        messages.success(request,'✅ تم الحفظ')
        return redirect('suppliers:detail', pk=pk)
    return render(request,'suppliers/form.html',{'s':s,'action':'edit','wilayas':WILAYAS})
