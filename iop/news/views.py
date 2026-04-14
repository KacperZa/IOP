
from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.urls import reverse_lazy
from django.core.paginator import Paginator 
import uuid
from django.conf import settings
from supabase_client import supabase

from .models import Articles
from .forms import ArticlesForm

def upload_image(file):
    extension = file.name.split('.')[-1]
    file_name = f"{uuid.uuid4()}.{extension}"

    supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
        path=file_name,
        file=file.read(),
        file_options={'content-type': file.content_type}
    )

    return supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(file_name)

def news_home(request):
    articles_list = Articles.objects.all().order_by('-published_at')
    
    paginator = Paginator(articles_list, 6) 
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    return render(request, 'news/index.html', {'news': news})

@login_required
def news_create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST, request.FILES)      
        if form.is_valid():
            ogloszenie = form.save(commit=False)
            ogloszenie.autor = request.user

            if 'image' in request.FILES:
                ogloszenie.image = upload_image(request.FILES['image'])

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

    def form_valid(self, form):
        if 'image' in self.request.FILES:
            form.instance.image = upload_image(self.request.FILES['image'])
        return super().form_valid(form)

class NewsDeleteView(DeleteView):
    model = Articles
    template_name = 'news/delete.html'
    success_url = reverse_lazy('home')