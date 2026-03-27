# core/models.py
from django.db import models
from django.contrib.auth.models import User

ROLES = [
    ('admin',   'مدير الكلية'),
    ('wasail',  'مسؤول الوسائل'),
    ('makhzan', 'أمين المخزن'),
    ('chef',    'رئيس مصلحة'),
]

class UserProfile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role       = models.CharField(max_length=20, choices=ROLES, default='chef')
    department = models.CharField(max_length=200, blank=True)
    phone      = models.CharField(max_length=20, blank=True)
    title      = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'ملف المستخدم'
        verbose_name_plural = 'ملفات المستخدمين'

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_role_display()})"

    def is_admin(self):   return self.role == 'admin'
    def is_wasail(self):  return self.role in ('admin','wasail')
    def is_makhzan(self): return self.role in ('admin','wasail','makhzan')
