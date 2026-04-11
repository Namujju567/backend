from django.db import models

STATUS_CHOICES = [('active', 'Active'), ('resolved', 'Resolved')]
SEVERITY_CHOICES = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]


class Alert(models.Model):
    title = models.CharField(max_length=256)
    device = models.CharField(max_length=128)
    location = models.CharField(max_length=128, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    dismissed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.severity}"

    class Meta:
        ordering = ['-time']
