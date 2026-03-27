# offices/models.py
from django.db import models

OFFICE_TYPES = [
    ('admin','مكتب إداري'),('service','مصلحة'),
    ('hall','قاعة دراسية'),('lecture','قاعة محاضرات'),
    ('store','مخزن'),('library','مكتبة'),
    ('lab','مختبر'),('common','مرافق مشتركة'),
]

class Office(models.Model):
    code       = models.CharField(max_length=20, unique=True)
    name       = models.CharField(max_length=300)
    name_fr    = models.CharField(max_length=300, blank=True)
    office_type= models.CharField(max_length=20, choices=OFFICE_TYPES, default='admin')
    floor      = models.CharField(max_length=50, blank=True)
    building   = models.CharField(max_length=50, blank=True)
    surface    = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    capacity   = models.IntegerField(null=True, blank=True)
    phone      = models.CharField(max_length=20, blank=True)
    email      = models.EmailField(blank=True)
    department = models.CharField(max_length=300, blank=True)
    notes      = models.TextField(blank=True)
    active     = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'مكتب'; verbose_name_plural = 'المكاتب والمحلات'
        ordering = ['code']

    def __str__(self): return f"{self.code} — {self.name}"

    def current_manager(self):
        return self.managers.filter(is_current=True).first()


class OfficeManager(models.Model):
    office        = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='managers')
    manager_name  = models.CharField(max_length=200)
    manager_title = models.CharField(max_length=200)
    manager_phone = models.CharField(max_length=20, blank=True)
    manager_email = models.EmailField(blank=True)
    start_date    = models.DateField()
    end_date      = models.DateField(null=True, blank=True)
    is_current    = models.BooleanField(default=True)
    notes         = models.TextField(blank=True)

    class Meta:
        verbose_name = 'مسؤول مكتب'; verbose_name_plural = 'مسؤولو المكاتب'

    def __str__(self): return f"{self.manager_name} — {self.office.name}"
