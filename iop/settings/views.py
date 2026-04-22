import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from news.models import Articles
from .forms import ProfileForm, AvatarForm
from supabase_client import supabase 

# Create your views here.
#settings page
@login_required
def settings(request):
    profile = request.user.profile
    print("avatar_url w settings view:", profile.avatar_url)

    return render(request, 'settings/settings.html', {'profile': profile})

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
    profile = request.user.profile

    if request.method == 'POST':
    #     profile_form = ProfileForm(request.POST, instance=profile)
    #     avatar_form = AvatarForm(request.FILES)
    #     print("avatar_form errors:", avatar_form.errors)
    #     print("avatar_form valid:", avatar_form.is_valid())
    #     print("FILES", request.FILES)

    #     if profile_form.is_valid():
    #         profile_form.save()

        if 'avatar' in request.FILES:
            file = request.FILES['avatar']
            ext = file.name.split('.')[-1]
            filename = f"{request.user.id}/{uuid.uuid4()}.{ext}"

            supabase.storage.from_('avatars').upload(
                filename,
                file.read(),
                {"content-type": file.content_type}
            )
            print("przed: ", profile.avatar_url)
            url = supabase.storage.from_('avatars').get_public_url(filename)
            profile.avatar_url = url 
            profile.save()
            print("avatar save: ", profile.avatar_url)
            
            # print("po: ", profile.objects.get(user=request.user).avatar_url)

    return redirect('settings')

def user_profile(request, username):
    user = get_object_or_404(User,username=username)
    articles = Articles.objects.filter(autor=user).order_by('-published_at')

    return render(request, 'settings/profile.html', {
        'profile_user': user,
        'articles': articles,
        'articles_count': articles.count(),
    })