from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


@csrf_exempt
def bootstrap_superadmin(request):
    """Temporary endpoint to create SSEMATA superadmin. DELETE THIS AFTER USE."""
    try:
        # Delete any existing conflicts
        User.objects.filter(username__iexact='SSEMATA').delete()
        User.objects.filter(email='ssematasabira24@gmail.com').delete()
        
        # Create fresh
        user = User.objects.create_superuser(
            username='SSEMATA',
            email='ssematasabira24@gmail.com',
            password='sabira@25',
            first_name='SSEMATA',
            last_name='SABIRA',
        )
        user.is_active = True
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Superadmin SSEMATA created successfully',
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
