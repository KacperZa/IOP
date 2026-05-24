# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages  
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Sum  

from settings.forms import RegisterForm
from news.models import Articles
from news.models import Ulubione

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

    print(values)
    return render(request, "main/ogloszenia.html", {
        'news': values, 
        'user_ulubione_ids': user_ulubione_ids,
        'total_views_sum': total_views,
        'total_favs_sum': total_favs     
    })


def about(request):
    return render(request, "main/about.html")


def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
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
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "main/users/register.html", {'form': form})


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