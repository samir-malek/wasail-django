# نظام الوسائل العامة — Django
## كلية الحقوق والعلوم السياسية — جامعة محمد البشير الإبراهيمي

### التشغيل المحلي
```bash
pip install -r requirements.txt
python manage.py migrate
python setup_data.py
python manage.py runserver
```
ثم افتح: http://localhost:8000
- اسم الدخول: `admin` | كلمة المرور: `admin123`

### النشر على Railway
1. ارفع على GitHub
2. اذهب إلى railway.app وأنشئ مشروعاً جديداً من GitHub
3. أضف قاعدة بيانات PostgreSQL
4. أضف متغيرات البيئة:
   - `SECRET_KEY` = مفتاح عشوائي طويل
   - `DATABASE_URL` = يُنسخ تلقائياً من PostgreSQL
   - `DEBUG` = False
   - `ALLOWED_HOSTS` = your-app.railway.app
5. سيُنشر تلقائياً

### الأدوار
| الدور | الصلاحيات |
|-------|-----------|
| admin | كل الصفحات |
| wasail | مسؤول الوسائل — كل شيء ما عدا إدارة المستخدمين |
| makhzan | أمين المخزن — استلام + تنفيذ السندات |
| chef | رئيس مصلحة — طلب + تأكيد الاستلام |
