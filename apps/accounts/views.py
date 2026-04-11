from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json

@csrf_exempt
def check_availability(request):
    """GET /api/accounts/check/?username=x&email=y"""
    username = request.GET.get('username', '').strip()
    email    = request.GET.get('email', '').strip()
    result   = {}

    if username:
        result['username_taken'] = User.objects.filter(username=username).exists()

    if email:
        try:
            validate_email(email)
            result['email_valid'] = True
        except ValidationError:
            result['email_valid'] = False
        result['email_taken'] = User.objects.filter(email=email).exists() if result.get('email_valid') else False

    return JsonResponse(result)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('full_name', '').split(' ', 1)
            first_name = full_name[0] if full_name else ''
            last_name = full_name[1] if len(full_name) > 1 else ''
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)

            user = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name
            )
            login(request, user)
            return JsonResponse({
                'message': 'Account created successfully',
                'user': {
                    'id': user.id, 'username': user.username,
                    'full_name': f"{user.first_name} {user.last_name}".strip(),
                    'email': user.email
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = authenticate(request, username=data.get('username'), password=data.get('password'))
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'message': 'Login successful',
                    'user': {
                        'id': user.id, 'username': user.username,
                        'full_name': f"{user.first_name} {user.last_name}".strip(),
                        'email': user.email
                    }
                })
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def me(request):
    if request.user.is_authenticated:
        u = request.user
        return JsonResponse({
            'id': u.id, 'username': u.username,
            'full_name': f"{u.first_name} {u.last_name}".strip(),
            'email': u.email
        })
    return JsonResponse({'error': 'Not authenticated'}, status=401)
