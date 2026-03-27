# transfers/models.py
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product
from offices.models import Office

STATUS_CHOICES = [
    ('pending','بانتظار الموافقة'),('approved','موافق عليه'),
    ('executed','منفَّذ'),('received','مستلَم'),('rejected','مرفوض'),
]
PRIORITY_CHOICES = [('normal','عادي'),('urgent','عاجل'),('critical','مستعجل')]
TYPE_CHOICES = [
    ('normal','تحويل عادي'),('emergency','تحويل طارئ'),
    ('internal','تحويل داخلي'),('return','استرجاع'),
]

class Transfer(models.Model):
    number           = models.CharField(max_length=20, unique=True, editable=False)
    transfer_type    = models.CharField(max_length=20, choices=TYPE_CHOICES, default='normal')
    requesting_office= models.ForeignKey(Office, on_delete=models.PROTECT, null=True, blank=True)
    requesting_dept  = models.CharField(max_length=300)
    requested_by     = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transfers_requested')
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority         = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    approved_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers_approved')
    approved_at      = models.DateTimeField(null=True, blank=True)
    executed_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers_executed')
    executed_at      = models.DateTimeField(null=True, blank=True)
    received_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers_received')
    received_at      = models.DateTimeField(null=True, blank=True)
    notes            = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'سند تحويل'; verbose_name_plural = 'سندات التحويل'
        ordering = ['-created_at']

    def __str__(self): return self.number

    def save(self, *args, **kwargs):
        if not self.number:
            from django.utils import timezone
            year  = timezone.now().year
            last  = Transfer.objects.filter(number__startswith=f'ST-{year}-').order_by('-number').first()
            if last:
                try:    seq = int(last.number.split('-')[-1]) + 1
                except: seq = 1
            else: seq = 1
            self.number = f'ST-{year}-{str(seq).zfill(3)}'
        super().save(*args, **kwargs)

    def status_badge(self):
        colors = {
            'pending':'warning','approved':'primary',
            'executed':'info','received':'success','rejected':'danger'
        }
        return colors.get(self.status,'secondary')


class TransferItem(models.Model):
    transfer      = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='items')
    product       = models.ForeignKey(Product, on_delete=models.PROTECT)
    requested_qty = models.DecimalField(max_digits=12, decimal_places=2)
    approved_qty  = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    delivered_qty = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notes         = models.TextField(blank=True)

    class Meta:
        verbose_name = 'مادة سند'; verbose_name_plural = 'مواد السند'

    def __str__(self): return f"{self.transfer.number} — {self.product.name}"
