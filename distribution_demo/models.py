# C:\DMP\DMP\distribution_demo\models.py
from django.db import models
from django.utils import timezone

class SimulatedRelease(models.Model):
    """
    A very simple model to represent a release we want to "distribute".
    In a real scenario, this would link to your actual Recording/Release models
    from Django Music Publisher.
    """
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    release_date = models.DateField(default=timezone.now)
    is_distributed = models.BooleanField(default=False)
    last_distribution_attempt = models.DateTimeField(null=True, blank=True)
    distribution_status = models.CharField(max_length=100, default='Pending') # e.g., 'Pending', 'Sent', 'Failed'

    def __str__(self):
        return f"{self.title} by {self.artist_name}"

    class Meta:
        verbose_name = "Simulated Release"
        verbose_name_plural = "Simulated Releases"