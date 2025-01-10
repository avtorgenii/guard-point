from django.db import models



class Worker(models.Model):
    # Attributes
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    card = models.CharField(max_length=100, null=True)  # Store integers, separated by coma
    created_at = models.DateTimeField(auto_now_add=True)


class ScanLog(models.Model):
    class ScanType(models.IntegerChoices):
        ENTRANCE = 1, 'Entrance'
        EXIT = 0, 'Exit'

    class ScanResult(models.IntegerChoices):
        SUCCESSFUL = 1, 'Successful'
        DENIED = 0, 'Denied'

    # Attributes
    card = models.CharField(max_length=100)  # Store integers, separated by coma
    worker_full_name = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    scan_type = models.BooleanField(null=True,
                                       choices=tuple(map(lambda x: (bool(x[0]), x[1]), ScanType.choices)))
    scan_result = models.BooleanField(null=True,
                                       choices=tuple(map(lambda x: (bool(x[0]), x[1]), ScanResult.choices)))

    # Manager
    worker = models.ForeignKey('Worker', on_delete=models.SET_DEFAULT, related_name='scanlog', null=True, default=None)

    def save(self, *args, **kwargs):
        # Set the worker_full_name field if the worker is available
        if self.worker:
            self.worker_full_name = f"{self.worker.name} {self.worker.surname}"

        super().save(*args, **kwargs)

    class Meta:
        # verbose_name = 'Famous men' - for admin panel - very inconvenient
        # verbose_name_plural = 'Famous men'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]

class CardChange(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    card_change_in_progress = models.BooleanField(default=True)




