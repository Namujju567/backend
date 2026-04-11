from django.db import models

SEVERITY_CHOICES = [
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
]


class KPI(models.Model):
    label = models.CharField(max_length=64)
    value = models.CharField(max_length=32)
    change = models.CharField(max_length=16)
    up = models.BooleanField(default=True)
    color = models.CharField(max_length=32, default='#000000')

    def __str__(self):
        return f"{self.label}: {self.value}"


class Sensor(models.Model):
    label = models.CharField(max_length=64)
    value = models.CharField(max_length=32)
    pct = models.PositiveSmallIntegerField()
    color = models.CharField(max_length=32, default='#000000')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} {self.value}"


class Device(models.Model):
    name = models.CharField(max_length=128)
    status = models.CharField(max_length=32)
    battery = models.PositiveSmallIntegerField()
    color = models.CharField(max_length=32, default='#000000')
    location = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.status})"


class Alert(models.Model):
    title = models.CharField(max_length=256)
    device = models.CharField(max_length=128)
    time = models.DateTimeField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.severity}"
