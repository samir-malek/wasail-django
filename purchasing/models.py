from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product
from suppliers.models import Supplier

PO_STATUS = [
    ('draft','مسودة'),('pending','بانتظار الموافقة'),
    ('approved','معتمد'),('ordered','تم الطلب'),
    ('received','مستلَم'),('cancelled','ملغى'),
]

class PurchaseOrder(models.Model):
    number        = models.CharField(max_length=20, unique=True, editable=False)
    supplier      = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    status        = models.CharField(max_length=15, choices=PO_STATUS, default='pending')
    priority      = models.CharField(max_length=20, default='عادي')
    requested_by  = models.ForeignKey(User, on_delete=models.PROTECT, related_name='purchase_orders')
    approved_by   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_orders')
    approved_at   = models.DateTimeField(null=True, blank=True)
    expected_delivery = models.DateField(null=True, blank=True)
    total_amount  = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    notes         = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'طلب شراء'; verbose_name_plural = 'طلبات الشراء'
        ordering = ['-created_at']

    def __str__(self): return self.number

    def save(self, *args, **kwargs):
        if not self.number:
            from django.utils import timezone
            year = timezone.now().year
            last = PurchaseOrder.objects.filter(number__startswith=f'BC-{year}-').order_by('-number').first()
            seq  = (int(last.number.split('-')[-1]) + 1) if last else 1
            self.number = f'BC-{year}-{str(seq).zfill(3)}'
        super().save(*args, **kwargs)

    def status_badge(self):
        return {'draft':'secondary','pending':'warning','approved':'success',
                'ordered':'primary','received':'info','cancelled':'danger'}.get(self.status,'secondary')


class PurchaseItem(models.Model):
    order         = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product       = models.ForeignKey(Product, on_delete=models.PROTECT)
    requested_qty = models.DecimalField(max_digits=12, decimal_places=2)
    received_qty  = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit_price    = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_price   = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    notes         = models.TextField(blank=True)

    def __str__(self): return f"{self.order.number} - {self.product.name}"


class Invoice(models.Model):
    number         = models.CharField(max_length=20, unique=True, editable=False)
    invoice_number = models.CharField(max_length=50)
    date           = models.DateField()
    supplier       = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount   = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    received_by    = models.ForeignKey(User, on_delete=models.PROTECT, related_name='invoices_received')
    notes          = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'فاتورة'; verbose_name_plural = 'الفواتير'
        ordering = ['-created_at']

    def __str__(self): return f"{self.number} - {self.invoice_number}"

    def save(self, *args, **kwargs):
        if not self.number:
            from django.utils import timezone
            year = timezone.now().year
            last = Invoice.objects.filter(number__startswith=f'FAC-{year}-').order_by('-number').first()
            seq  = (int(last.number.split('-')[-1]) + 1) if last else 1
            self.number = f'FAC-{year}-{str(seq).zfill(3)}'
        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    invoice    = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity   = models.DecimalField(max_digits=12, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_price= models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self): return f"{self.invoice.number} - {self.product.name}"
