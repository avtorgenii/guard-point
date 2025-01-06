from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import CharField


class Worker(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, 'Active'
        INACTIVE = 0, 'Inactive'

    # Attributes
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    card = models.CharField(max_length=100)  # Store list of integers
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=Status.INACTIVE,
                                       choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)))


class ScanLog(models.Model):
    class ScanType(models.IntegerChoices):
        ENTRANCE = 1, 'Entrance'
        EXIT = 0, 'Exit'

    class ScanResult(models.IntegerChoices):
        SUCCESSFUL = 1, 'Successful'
        DENIED = 0, 'Denied'

    # Attributes
    card = models.CharField(max_length=100)  # Store list of integers
    timestamp = models.DateTimeField(auto_now_add=True)
    scan_type = models.BooleanField(null=True,
                                       choices=tuple(map(lambda x: (bool(x[0]), x[1]), ScanType.choices)))
    scan_result = models.BooleanField(null=True,
                                       choices=tuple(map(lambda x: (bool(x[0]), x[1]), ScanResult.choices)))

    # Manager
    worker = models.ForeignKey('Worker', on_delete=models.PROTECT, related_name='scanlog', null=True)


    class Meta:
        # verbose_name = 'Famous men' - for admin panel - very inconvenient
        # verbose_name_plural = 'Famous men'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]





