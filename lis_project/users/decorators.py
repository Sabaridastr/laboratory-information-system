from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                user_groups = request.user.groups.values_list('name', flat=True)

                if any(role in user_groups for role in allowed_roles):
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, "You are not authorized to access this page")
                    return redirect('dashboard')
            else:
                return redirect('login')
        return wrapper
    return decorator