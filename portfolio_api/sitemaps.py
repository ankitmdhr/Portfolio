from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import PortfolioItem, Post

class PortfolioItemSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return PortfolioItem.objects.all()

    def lastmod(self, obj):
        # FIX: Changed from obj.created_at to obj.date_created
        return obj.date_created

class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class StaticViewSitemap(Sitemap):
    """Sitemap for static pages like 'services'."""
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        # Return a list of URL names for your static pages
        return ['portfolio_page', 'services_page', 'blog_list']

    def location(self, item):
        return reverse(item)