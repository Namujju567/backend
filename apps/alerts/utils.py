from .models import Alert


def create_alert(title, device, message, severity='Medium', location='Main Entrance', status='active'):
    return Alert.objects.create(
        title=title,
        device=device,
        message=message,
        severity=severity,
        location=location,
        status=status,
    )
