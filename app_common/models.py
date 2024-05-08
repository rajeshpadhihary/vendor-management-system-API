from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, Count, F
from django.utils import timezone
from datetime import timedelta

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50,default="pending")
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def is_on_time(self):
        return self.delivery_date <= timezone.now()

    @property
    def is_fulfilled(self):
        return self.status == 'completed' and (not self.issue_date or self.issue_date <= self.delivery_date)

    @property
    def response_time(self):
        if self.acknowledgment_date and self.issue_date:
            return (self.acknowledgment_date - self.issue_date).total_seconds() / 3600  # Convert to hours
        return 0

    def __str__(self):
        return self.po_number

@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs):
    vendor = instance.vendor

    if instance.status == 'completed':
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        vendor.on_time_delivery_rate = completed_pos.filter(delivery_date__lte=timezone.now()).count() / completed_pos.count()

        quality_rating_avg = completed_pos.exclude(quality_rating__isnull=True).aggregate(Avg('quality_rating'))['quality_rating__avg']
        vendor.quality_rating_avg = quality_rating_avg or 0

    if instance.acknowledgment_date and instance.issue_date:
        try:
            response_times = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False, issue_date__isnull=False).aggregate(Avg(F('acknowledgment_date') - F('issue_date')))['acknowledgment_date__avg']
            vendor.average_response_time = response_times or 0
        except ZeroDivisionError:
            pass

    try:
        fulfilled_pos = PurchaseOrder.objects.filter(vendor=vendor)
        vendor.fulfillment_rate = fulfilled_pos.filter(status='completed').count() / fulfilled_pos.count()
    except ZeroDivisionError:
        pass

    vendor.save()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
