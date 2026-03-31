from django.shortcuts import render, redirect
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
#settings page
@login_required
def settings(request):
    return render(request, 'settings/settings.html')

# Password change
@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, 'Stare hasło nieprawidłowe.')
        elif new_password1 != new_password2:
            messages.error(request, "Hasła nie są identyczne")
        elif len(new_password1) < 8:
            messages.error(request, 'Hasło powinno mieć przynajmniej 8 znaków.')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)  # keep user logged in
            messages.success(request, 'Hasło zostało zmienione.')
    return redirect('settings')

# account deletion
@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.user.check_password(password):
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, 'Konto zostało usunięte.')
            return redirect('home')
        else:
            messages.error(request, 'Nieprawidłowe hasło.')
    return redirect('settings')

# Change username
@login_required
def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        if new_username:
            if request.user.__class__.objects.filter(username=new_username).exists():
                messages.error(request, 'Ta nazwa użytkownika jest zajęta.')
            else:
                request.user.username = new_username
                request.user.save()
                messages.success(request, 'Nazwa użytkownika została zmieniona.')
    return redirect('settings')

# PFP change
@login_required
def change_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        profile = request.user.profile
        profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, 'Profile picture updated.')
    return redirect('settings')