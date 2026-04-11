from django.db import models


class SystemSettings(models.Model):
    # API
    api_endpoint     = models.URLField(default='http://localhost:8000')
    api_key          = models.CharField(max_length=256, blank=True)
    poll_interval    = models.PositiveIntegerField(default=30)

    # Device
    default_location  = models.CharField(max_length=128, default='Main Entrance')
    device_timeout    = models.PositiveIntegerField(default=60)
    temperature_unit  = models.CharField(max_length=16, default='Celsius')
    auto_reconnect    = models.BooleanField(default=True)

    # System
    system_online     = models.BooleanField(default=True)

    # Notifications
    alert_email       = models.EmailField(blank=True)
    low_threshold     = models.PositiveSmallIntegerField(default=20)
    email_alerts      = models.BooleanField(default=True)
    sms_alerts        = models.BooleanField(default=False)
    push_alerts       = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'System Settings'

    def __str__(self):
        return 'System Settings'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


POWER_GROUP_CHOICES = [
    ('devices', 'Devices'),
    ('sensors', 'Sensors'),
    ('boards',  'Boards'),
    ('other',   'Other'),
]


class PowerDevice(models.Model):
    name   = models.CharField(max_length=128)
    group  = models.CharField(max_length=16, choices=POWER_GROUP_CHOICES)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({'On' if self.status else 'Off'})"
