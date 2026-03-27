from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Office, OfficeManager
import datetime

@login_required
def office_list(request):
    offices = Office.objects.filter(active=True).prefetch_related('managers')
    return render(request,'offices/list.html',{'offices':offices})

@login_required
def office_add(request):
    if request.method == 'POST':
        try:
            Office.objects.create(
                code=request.POST['code'].upper().strip(),
                name=request.POST['name'].strip(),
                name_fr=request.POST.get('name_fr','').strip(),
                office_type=request.POST.get('office_type','admin'),
                floor=request.POST.get('floor','').strip(),
                building=request.POST.get('building','').strip(),
                surface=request.POST.get('surface') or None,
                capacity=request.POST.get('capacity') or None,
                phone=request.POST.get('phone','').strip(),
                email=request.POST.get('email','').strip(),
                department=request.POST.get('department','').strip(),
                notes=request.POST.get('notes','').strip(),
            )
            messages.success(request,'✅ تمت الإضافة')
            return redirect('offices:list')
        except Exception as e:
            messages.error(request, f'❌ {e}')
    from config_data import OFFICE_TYPES, DEPARTMENTS
    return render(request,'offices/form.html',{'office_types':OFFICE_TYPES,'departments':DEPARTMENTS})

@login_required
def office_detail(request, pk):
    o = get_object_or_404(Office, pk=pk)
    managers = o.managers.order_by('-start_date')
    return render(request,'offices/detail.html',{'o':o,'managers':managers})

@login_required
def managers(request):
    mgrs = OfficeManager.objects.filter(is_current=True).select_related('office')
    return render(request,'offices/managers.html',{'mgrs':mgrs})

@login_required
def assign_manager(request):
    if request.method == 'POST':
        office = get_object_or_404(Office, pk=request.POST['office'])
        start  = request.POST.get('start_date', str(datetime.date.today()))
        # إنهاء المسؤول الحالي
        OfficeManager.objects.filter(office=office, is_current=True).update(
            is_current=False, end_date=start)
        OfficeManager.objects.create(
            office=office,
            manager_name=request.POST['manager_name'].strip(),
            manager_title=request.POST['manager_title'].strip(),
            manager_phone=request.POST.get('manager_phone','').strip(),
            manager_email=request.POST.get('manager_email','').strip(),
            start_date=start,
            is_current=True,
        )
        messages.success(request, '✅ تم التعيين')
        return redirect('offices:managers')
    offices = Office.objects.filter(active=True)
    return render(request,'offices/assign.html',{'offices':offices})
