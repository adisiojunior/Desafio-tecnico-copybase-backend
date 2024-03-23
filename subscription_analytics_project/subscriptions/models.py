from django.db import models

class Subscriber(models.Model):
    quantity_changes = models.IntegerField()
    billing_every_days = models.IntegerField()
    start_date = models.DateTimeField()
    status = models.CharField(max_length=20)
    date_status = models.DateTimeField()
    cancellation_date = models.DateField(null=True, blank=True)
    value = models.FloatField()
    next_cycle = models.DateField()
    subscriber_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.subscriber_id

