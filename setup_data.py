"""
سكريبت تهيئة البيانات الأولية
شغّله مرة واحدة بعد التثبيت:
  python setup_data.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wasail.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile
from catalog.models import Category, Unit
from offices.models import Office

# المدير الافتراضي
if not User.objects.filter(username='admin').exists():
    u = User.objects.create_superuser('admin','admin@faculty.dz','admin123')
    u.first_name='مدير'; u.last_name='النظام'; u.save()
    UserProfile.objects.filter(user=u).update(
        role='admin', department='مصلحة الوسائل العامة', title='المدير'
    )
    print("✅ تم إنشاء حساب admin")

# الفئات
CATS = [
    ('قرطاسية ولوازم مكتبية','🖊️'),('مواد النظافة','🧹'),
    ('أجهزة حاسوبية','💻'),('أجهزة مكتبية','🖨️'),
    ('أثاث','🪑'),('مواد الطباعة','📄'),
    ('مواد الضيافة','☕'),('كهرباء وإنارة','💡'),
    ('أدوات وعتاد','🔧'),('أخرى','📦'),
]
for name, icon in CATS:
    Category.objects.get_or_create(name=name, defaults={'icon':icon})
print(f"✅ {len(CATS)} فئات منتجات")

# الوحدات
UNITS = [
    ('قطعة','قط'),('علبة','عب'),('رزمة','رز'),
    ('لتر','ل'),('كيلوغرام','كغ'),('رول','رول'),
    ('كارتون','كرت'),('مجموعة','مج'),('متر','م'),('حبة','حبة'),
]
for name, symbol in UNITS:
    Unit.objects.get_or_create(name=name, defaults={'symbol':symbol})
print(f"✅ {len(UNITS)} وحدات قياس")

# المكاتب الافتراضية
OFFICES = [
    ('OFF-001','الأمانة العامة','Secrétariat Général','admin','الطابق الأول','A'),
    ('OFF-002','مكتب الأستاذة','Bureau du Professorat','admin','الطابق الأول','A'),
    ('OFF-003','مصلحة التدريس','Service Enseignement','service','الطابق الثاني','B'),
    ('OFF-004','مصلحة البيداغوجيا','Service Pédagogie','service','الطابق الثاني','B'),
    ('OFF-005','مكتبة الكلية','Bibliothèque','library','الطابق الأرضي','A'),
    ('OFF-006','مصلحة الماستر والدكتوراه','Service Master & Doctorat','service','الطابق الثالث','C'),
    ('OFF-007','مصلحة الوسائل العامة','Service des Moyens','service','الطابق الأرضي','A'),
    ('OFF-008','المخزن الرئيسي','Magasin Principal','store','الطابق الأرضي','A'),
]
for code,name,name_fr,typ,floor,building in OFFICES:
    Office.objects.get_or_create(code=code, defaults={
        'name':name,'name_fr':name_fr,'office_type':typ,
        'floor':floor,'building':building,'department':name,
    })
print(f"✅ {len(OFFICES)} مكاتب افتراضية")
print("\n🎉 النظام جاهز! افتح: http://localhost:8000")
print("   اسم الدخول: admin | كلمة المرور: admin123")
