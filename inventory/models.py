from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product

class InventorySession(models.Model):
    number       = models.CharField(max_length=20, unique=True, editable=False)
    date         = models.DateTimeField(auto_now_add=True)
    scope        = models.CharField(max_length=200, default='جرد شامل')
    conducted_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='inventory_sessions')
    validated_by = models.CharField(max_length=200, blank=True)
    status       = models.CharField(max_length=20, default='completed')
    notes        = models.TextField(blank=True)

    class Meta:
        verbose_name = 'جلسة جرد'; verbose_name_plural = 'جلسات الجرد'
        ordering = ['-date']

    def __str__(self): return self.number

    def save(self, *args, **kwargs):
        if not self.number:
            from django.utils import timezone
            year = timezone.now().year
            last = InventorySession.objects.filter(number__startswith=f'INV-{year}-').order_by('-number').first()
            seq  = (int(last.number.split('-')[-1]) + 1) if last else 1
            self.number = f'INV-{year}-{str(seq).zfill(3)}'
        super().save(*args, **kwargs)

    def summary(self):
        items = self.items.all()
        ok  = items.filter(difference=0).count()
        neg = items.filter(difference__lt=0).count()
        pos = items.filter(difference__gt=0).count()
        return {'total':items.count(),'ok':ok,'shortage':neg,'surplus':pos}


class InventoryItem(models.Model):
    session        = models.ForeignKey(InventorySession, on_delete=models.CASCADE, related_name='items')
    product        = models.ForeignKey(Product, on_delete=models.PROTECT)
    theoretical_qty= models.DecimalField(max_digits=12, decimal_places=2)
    actual_qty     = models.DecimalField(max_digits=12, decimal_places=2)
    difference     = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes          = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.difference = self.actual_qty - self.theoretical_qty
        super().save(*args, **kwargs)

    def __str__(self): return f"{self.session.number} - {self.product.name}"
