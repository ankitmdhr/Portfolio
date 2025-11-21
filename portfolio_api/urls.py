from django.urls import path
from . import views

urlpatterns = [
    # Main page
    path('', views.portfolio_page_view, name='portfolio_page'),
    
    # Services page
    path('services/', views.services_page_view, name='services_page'),
    
    # Project detail page
    path('work/<slug:slug>/', views.project_detail_view, name='project_detail'),
    
    # Blog list page
    path('blog/', views.blog_list_view, name='blog_list'),
    
    # Blog detail page
    path('blog/<slug:slug>/', views.blog_detail_view, name='blog_detail'),
]

