from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def admin_login(request):
    """
    View for admin login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin_app:admin_dashboard')
        else:
            return render(request, 'admin/login.html', {'error': 'Invalid username or password'})

    return render(request, 'admin/login.html')

@login_required
def admin_dashboard(request):
    """
    View for admin dashboard.
    """
    return render(request, 'admin/dashboard.html')

def admin_logout(request):
    """
    View for admin logout.
    """
    logout(request)
    return redirect('admin_app:admin_login')
