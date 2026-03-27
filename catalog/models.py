# catalog/models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name       = models.CharField(max_length=200, unique=True, verbose_name='الاسم')
    name_fr    = models.CharField(max_length=200, blank=True, verbose_name='بالفرنسية')
    icon       = models.CharField(max_length=10, default='📦')
    description= models.TextField(blank=True)
    active     = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'فئة'; verbose_name_plural = 'الفئات'
        ordering = ['name']

    def __str__(self): return self.name
    def product_count(self): return self.product_set.filter(active=True).count()


class Unit(models.Model):
    name    = models.CharField(max_length=100, unique=True, verbose_name='الاسم')
    name_fr = models.CharField(max_length=100, blank=True, verbose_name='بالفرنسية')
    symbol  = models.CharField(max_length=20, verbose_name='الرمز')
    active  = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'وحدة'; verbose_name_plural = 'وحدات القياس'
        ordering = ['name']

    def __str__(self): return f"{self.name} ({self.symbol})"


class Product(models.Model):
    code          = models.CharField(max_length=50, unique=True, verbose_name='الرمز')
    name          = models.CharField(max_length=300, verbose_name='الاسم')
    name_fr       = models.CharField(max_length=300, blank=True, verbose_name='بالفرنسية')
    category      = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='الفئة')
    unit          = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name='الوحدة')
    min_stock     = models.DecimalField(max_digits=10, decimal_places=2, default=5, verbose_name='حد التنبيه')
    max_stock     = models.DecimalField(max_digits=10, decimal_places=2, default=100, verbose_name='الحد الأقصى')
    reorder_qty   = models.DecimalField(max_digits=10, decimal_places=2, default=20, verbose_name='كمية إعادة الطلب')
    brand         = models.CharField(max_length=200, blank=True, verbose_name='الماركة')
    model         = models.CharField(max_length=200, blank=True, verbose_name='الموديل')
    description   = models.TextField(blank=True, verbose_name='الوصف')
    specifications= models.TextField(blank=True, verbose_name='المواصفات')
    active        = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    created_by    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'منتج'; verbose_name_plural = 'المنتجات'
        ordering = ['name']

    def __str__(self): return f"{self.code} — {self.name}"

    def current_stock(self):
        from stock.models import Stock
        try:
            return self.stock.quantity
        except: return 0

    def stock_status(self):
        qty = self.current_stock()
        if qty == 0:              return 'نفد',    'danger'
        elif qty <= self.min_stock: return 'منخفض', 'warning'
        elif qty <= self.min_stock*2: return 'متوسط','info'
        else:                     return 'جيد',    'success'
