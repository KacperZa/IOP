

from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.urls import reverse_lazy

from .models import Articles
from .forms import ArticlesForm


def news_home(request):
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
            return redirect('home') 
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
    
    def get_object(self):
        obj = super().get_object()
        Articles.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        return obj

class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'news/update.html'
    form_class = ArticlesForm

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            kwargs['files'] = self.request.FILES
        return kwargs

class NewsDeleteView(DeleteView):
    model = Articles
    template_name = 'news/delete.html'
    success_url = reverse_lazy('home')