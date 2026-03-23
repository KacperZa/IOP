<<<<<<< HEAD
"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

=======
# Główny plik URL projektu 
from django.contrib import admin
from django.urls import path, include
>>>>>>> 4d969f5df22628a66df89df871fc2d28fe640761
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls), # default, part of django
    path('', include('main.urls')),
    path('news/', include('news.urls')), 
    path('forum/', include('forum.urls')) #delegating authority to an internal application to forum.urls that is needed to be created
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
=======
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('news/', include('news.urls')), 
    path('forum/', include('forum.urls')),
]

# To dodaje obsługę plików statycznych ORAZ zdjęć
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 4d969f5df22628a66df89df871fc2d28fe640761
