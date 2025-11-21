"""
URL configuration for portfolio_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
"""
URL configuration for portfolio_project project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve # Import the view to serve files

# Imports for Sitemap
from django.contrib.sitemaps.views import sitemap
from portfolio_api.sitemaps import PortfolioItemSitemap, PostSitemap, StaticViewSitemap
from portfolio_api.views import robots_txt_view

# Sitemap Configuration
sitemaps = {
    'portfolio': PortfolioItemSitemap,
    'blog': PostSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, 
         name='django.contrib.sitemaps.views.sitemap'),
         
    # robots.txt
    path('robots.txt', robots_txt_view),
    
    # TinyMCE
    path('tinymce/', include('tinymce.urls')),
    
    # Include your app's URLs
    path('', include('portfolio_api.urls')),
    
    # --- FIX: Force Django to serve media files in Production ---
    # This connects the /media/ URL to your persistent disk folder
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

# Serve static files during development (CSS/JS)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)