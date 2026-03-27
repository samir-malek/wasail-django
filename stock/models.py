# stock/models.py
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product

class Stock(models.Model):
    product      = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    quantity     = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reserved_qty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'مخزون'; verbose_name_plural = 'المخزون'

    def __str__(self): return f"{self.product.name}: {self.quantity}"
    def available(self): return self.quantity - self.reserved_qty

DIRECTION_CHOICES = [('in','دخول'),('out','خروج')]
REF_CHOICES = [('invoice','فاتورة'),('transfer','سند تحويل'),('inventory','جرد'),('adjustment','تسوية')]

class StockMovement(models.Model):
    date             = models.DateTimeField(auto_now_add=True)
    direction        = models.CharField(max_length=5, choices=DIRECTION_CHOICES)
    product          = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity         = models.DecimalField(max_digits=12, decimal_places=2)
    unit_cost        = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reference_type   = models.CharField(max_length=20, choices=REF_CHOICES, blank=True)
    reference_number = models.CharField(max_length=50, blank=True)
    from_location    = models.CharField(max_length=200, blank=True)
    to_location      = models.CharField(max_length=200, blank=True)
    notes            = models.TextField(blank=True)
    created_by       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'حركة مخزن'; verbose_name_plural = 'حركات المخزن'
        ordering = ['-date']

    def __str__(self): return f"{self.get_direction_display()} {self.product.name} {self.quantity}"
