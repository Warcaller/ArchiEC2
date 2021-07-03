from django.db import models

# Create your models here.
class Schedule(models.Model):
    stream_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    what = models.CharField(blank=True, null=True, max_length=24)
    description = models.TextField(blank=True, null=True, max_length=128)
    
    class Meta:
        ordering = ["stream_date", "start_time"]
