from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import PortfolioItem, Testimonial, Post, SiteConfiguration

def robots_txt_view(request):
    """
    Renders the robots.txt file.
    """
    return render(request, 'robots.txt', {}, content_type="text/plain")

def portfolio_page_view(request):
    """
    Handles logic for the main portfolio page (index.html).
    """
    message_sent = False
    
    if request.method == 'POST' and 'name' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        subject = f'New Contact Form Message from {name}'
        email_message = f"""
        You have received a new message from your portfolio website:

        Name: {name}
        Email: {email}
        Message:
        {message}
        """
        
        try:
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL, 
                [settings.RECIPIENT_EMAIL],  
                fail_silently=False,
            )
            message_sent = True
        except Exception as e:
            print(f"Error sending email: {e}")
            
        return redirect(request.path + '?message_sent=true#contact')

    message_sent = request.GET.get('message_sent') == 'true'

    # FIX: Changed '-created_at' to '-date_created' for PortfolioItem
    portfolio_items = PortfolioItem.objects.all().order_by('-date_created')
    
    # These models correctly use 'created_at'
    testimonials = Testimonial.objects.all().order_by('-created_at')
    latest_posts = Post.objects.all().order_by('-created_at')[:3] 
    
    context = {
        'portfolio_items': portfolio_items,
        'testimonials': testimonials,
        'latest_posts': latest_posts,
        'message_sent': message_sent,
    }
    return render(request, 'index.html', context)

def project_detail_view(request, slug):
    project = get_object_or_404(PortfolioItem, slug=slug)
    additional_images = project.additional_images.all()
    
    context = {
        'project': project,
        'additional_images': additional_images
    }
    return render(request, 'project_detail.html', context)

def services_page_view(request):
    return render(request, 'services.html')

# --- Blog Views ---
def blog_list_view(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'blog_list.html', context)

def blog_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post
    }
    return render(request, 'blog_detail.html', context)

def portfolio_page_view(request):
    # ... (Keep existing email/contact logic) ...
    message_sent = False
    
    if request.method == 'POST' and 'name' in request.POST:
        # ... (Keep existing email sending logic) ...
        pass # Placeholder to show where existing code is

    message_sent = request.GET.get('message_sent') == 'true'

    portfolio_items = PortfolioItem.objects.all().order_by('-date_created')
    testimonials = Testimonial.objects.all().order_by('-created_at')
    latest_posts = Post.objects.all().order_by('-created_at')[:3]
    
    # --- FETCH SITE CONFIG ---
    site_config = SiteConfiguration.objects.first()
    
    context = {
        'portfolio_items': portfolio_items,
        'testimonials': testimonials,
        'latest_posts': latest_posts,
        'message_sent': message_sent,
        'site_config': site_config, # Pass it to the template
    }
    return render(request, 'index.html', context)