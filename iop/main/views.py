# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce

import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages  
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Sum  
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from dotenv import load_dotenv

from django.conf import settings
from settings.forms import RegisterForm
from news.models import Articles
from news.models import Ulubione

load_dotenv(settings.BASE_DIR / '.env')


@login_required
def toggle_ulubione(request, ogloszenie_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Tylko POST'})
    
    ogloszenie = get_object_or_404(Articles, id=ogloszenie_id)
    ulubione, created = Ulubione.objects.get_or_create(
        user=request.user,
        ogloszenie=ogloszenie
    )
    if not created:
        ulubione.delete()

    return JsonResponse({
        'ulubione': created,
        'liczba': ogloszenie.ulubione.count(),
    })


def index(request):
    articles = Articles.objects.all()

    search_query = request.GET.get('search')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category_filter = request.GET.get('category')
    sort_by = request.GET.get('sort')

    if category_filter:
        articles = articles.filter(category=category_filter)
    if search_query:
        articles = articles.filter(title__icontains=search_query)
    if price_min:
        articles = articles.filter(price__gte=price_min)
    if price_max:
        articles = articles.filter(price__lte=price_max)

    if sort_by == 'price_asc':
        articles = articles.order_by('price') 
    elif sort_by == 'price_desc':
        articles = articles.order_by('-price') 
    else:
        articles = articles.order_by('-published_at') 

    user_ulubione_ids = []
    if request.user.is_authenticated:
        user_ulubione_ids = list(request.user.ulubione.values_list('ogloszenie_id', flat=True))

    return render(request, "main/index.html", {
        'articles': articles, 
        'user_ulubione_ids': user_ulubione_ids
    })



@never_cache
@login_required
def article(request):
    
    values = Articles.objects.filter(autor=request.user).order_by('-published_at')

    
    total_views = values.aggregate(Sum('views'))['views__sum'] or 0

    
    total_favs = Ulubione.objects.filter(ogloszenie__autor=request.user).count()

   
    user_ulubione_ids = list(
        request.user.ulubione.values_list('ogloszenie_id', flat=True)
    )

    show_verify = request.session.get('show_verify_banner', False)


    print(values)
    return render(request, "main/ogloszenia.html", {
        'news': values, 
        'user_ulubione_ids': user_ulubione_ids,
        'total_views_sum': total_views,
        'total_favs_sum': total_favs,
    })


def about(request):
    return render(request, "main/about.html")



def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        user = authenticate(
            username=request.POST["email"], password=request.POST["password"]
        )
        if user is not None:
            login(request, user)
            if request.session.get("next"):
                return redirect(request.session.pop("next"))

            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login_user")

    if request.GET.get("next"):
        request.session["next"] = request.GET["next"]

    return render(request, "main/users/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            send_verification_email(user, request, form.cleaned_data.get('email'))
            
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, "main/users/register.html", {'form': form})

def send_verification_email(user, request, to_email):
    try:
        mail_subject= "Aktywuj konto w serwisie IOP"
        message = render_to_string("main/template_activate_account.html", {
            'username': user.username,
            'domain': get_current_site(request).domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        })
        email = EmailMessage(mail_subject, message, to=[to_email])
        if email.send():
            request.session['show_verify_banner'] = True
            request.session['verify_email'] = to_email
        else:
            messages.error(request, f'Wystąpił problem podczas wysyłania linku aktywującego konto, sprawdź czy dobrze go napisałeś.')
    except Exception as e:
        print(f"EMAIL ERROR: {e}")
        raise

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user = None

    if user and not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        request.session['show_verify_banner'] = False

        login(request, user)

        messages.success(request, 'Dziękujemy za potwierdzenie adresu email. Życzymy miłego korzystania z naszego serwisu.')
        return redirect('/')
    else:
        messages.error(request, 'Link wygasł lub jest nieprawidłowy!')
    return redirect('homepage')

def logout_user(request):
    logout(request)
    return redirect("home")


def contact(request):
    return render(request, "main/contact.html")


def regulamin(request):
    return render(request, "main/regulamin.html")

def privacy(request):
    return render(request, "main/privacy.html")

@login_required
def favourites(request):
    fav_ids = list(
        request.user.ulubione.values_list('ogloszenie_id', flat=True)
    )
    news = Articles.objects.filter(id__in=fav_ids).order_by('-published_at')
    return render(request, 'main/favourites.html', {'news': news, 'user_ulubione_ids': fav_ids})