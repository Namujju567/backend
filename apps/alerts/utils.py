from .models import Alert


def create_alert(title, device, message, severity='Medium', location='Main Entrance', status='active'):
    # Suppress duplicate: skip if an active alert with same title+device already exists
    if Alert.objects.filter(title=title, device=device, status='active', dismissed=False).exists():
        return None
    return Alert.objects.create(
        title=title,
        device=device,
        message=message,
        severity=severity,
        location=location,
        status=status,
    )
