# suppliers/models.py
from django.db import models

SUPPLIER_TYPES = [
    ('public','مؤسسة عمومية'),('private','شركة خاصة'),
    ('sme','مؤسسة صغيرة'),('retail','تاجر تجزئة'),
    ('importer','مستورد'),('other','أخرى'),
]
RATINGS = [(i, '⭐'*i) for i in range(1,6)]
PAYMENT_TERMS = [
    ('cash','نقداً'),('30','30 يوم'),('60','60 يوم'),
    ('90','90 يوم'),('advance','دفع مسبق'),
]

class Supplier(models.Model):
    code          = models.CharField(max_length=20, unique=True)
    name          = models.CharField(max_length=300, verbose_name='الاسم')
    name_fr       = models.CharField(max_length=300, blank=True)
    supplier_type = models.CharField(max_length=20, choices=SUPPLIER_TYPES, default='private')
    phone         = models.CharField(max_length=20, blank=True)
    phone2        = models.CharField(max_length=20, blank=True)
    email         = models.EmailField(blank=True)
    fax           = models.CharField(max_length=20, blank=True)
    address       = models.TextField(blank=True)
    wilaya        = models.CharField(max_length=100, blank=True)
    nif           = models.CharField(max_length=50, blank=True, verbose_name='NIF')
    nis           = models.CharField(max_length=50, blank=True, verbose_name='NIS')
    rc            = models.CharField(max_length=50, blank=True, verbose_name='RC')
    bank_name     = models.CharField(max_length=200, blank=True)
    bank_account  = models.CharField(max_length=50, blank=True)
    payment_terms = models.CharField(max_length=10, choices=PAYMENT_TERMS, default='cash')
    delivery_days = models.IntegerField(default=7)
    rating        = models.IntegerField(choices=RATINGS, default=3)
    notes         = models.TextField(blank=True)
    active        = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'مورد'; verbose_name_plural = 'الموردون'
        ordering = ['name']

    def __str__(self): return f"{self.code} — {self.name}"
    def rating_stars(self): return '⭐' * self.rating


class SupplierContact(models.Model):
    supplier   = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='contacts')
    full_name  = models.CharField(max_length=200)
    position   = models.CharField(max_length=200, blank=True)
    phone      = models.CharField(max_length=20, blank=True)
    email      = models.EmailField(blank=True)
    notes      = models.TextField(blank=True)
    active     = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'جهة اتصال'; verbose_name_plural = 'جهات الاتصال'

    def __str__(self): return f"{self.full_name} ({self.supplier.name})"
