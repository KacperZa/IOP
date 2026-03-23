# Widoki dla ogłoszeń - obsługa zdjęć i formularzy
from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.db.models import F

from .models import Articles
from .forms import ArticlesForm

def news_home(request):
    # Pobieramy wszystkie ogłoszenia od najnowszych
    news = Articles.objects.all().order_by('-published_at')
    return render(request, 'news/index.html', {'news': news})

@login_required
def news_create(request):
    error = ''
    if request.method == 'POST':

        form = ArticlesForm(request.POST, request.FILES)      
        if form.is_valid():
            ogloszenie = form.save(commit=False)
            ogloszenie.autor = request.user
            ogloszenie.save() 
            return redirect('news_home')
        else:
            error = 'Formularz zawiera błędy'
    else:
        form = ArticlesForm()

    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'news/create.html', data)

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/show.html'
    context_object_name = 'article'
    
    # Aktualizowanie wyświetleń ogłoszenia
    def get_object(self):
        obj = super().get_object()
        Articles.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        return obj

class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'news/update.html'
    form_class = ArticlesForm
    
    # Dodajemy obsługę plików przy aktualizacji
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['files'] = self.request.FILES
        return kwargs

class NewsDeleteView(DeleteView):
    model = Articles
    template_name = 'news/delete.html'
    success_url = '/news/'