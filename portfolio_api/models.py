from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from tinymce.models import HTMLField

# --- 1. PORTFOLIO ITEM MODEL ---
class PortfolioItem(models.Model):
    """
    Represents a single project in your portfolio.
    """
    CATEGORY_CHOICES = (
        ('photography', 'Photography'),
        ('videography', 'Videography'),
        ('editing', 'Editing'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Project Title")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='photography')
    description = models.TextField(verbose_name="Detailed Description")
    
    # 1. Thumbnail/Cover Image (Required for video links, optional for direct video uploads)
    image_file = models.FileField(
        upload_to='portfolio_images/',
        blank=True, 
        null=True,
        verbose_name="Cover Image / Photo"
    )
    
    # 2. Direct Video Upload (Plays on your site)
    video_file = models.FileField(
        upload_to='portfolio_videos/',
        blank=True,
        null=True,
        verbose_name="Video File Upload (MP4)"
    )

    # 3. External Video Link (YouTube, Vimeo, etc.)
    video_url = models.URLField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name="External Video Link"
    )
    
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Portfolio Item"
        verbose_name_plural = "Portfolio Items"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    # --- Helper Method for Admin & Templates ---
    def is_media_video(self):
        """
        Returns True if there is a video file OR a video URL.
        """
        return bool(self.video_file) or bool(self.video_url)


# --- 2. GALLERY IMAGES MODEL ---
class AdditionalImage(models.Model):
    """
    Allows multiple extra images to be attached to a single PortfolioItem.
    """
    portfolio_item = models.ForeignKey(
        PortfolioItem, 
        related_name='additional_images', 
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='portfolio_gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Gallery Image for {self.portfolio_item.title}"


# --- 3. TESTIMONIAL MODEL ---
class Testimonial(models.Model):
    """
    Stores client feedback/reviews.
    """
    client_name = models.CharField(max_length=100)
    quote = models.TextField()
    company = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Testimonial from {self.client_name}"


# --- 4. BLOG POST MODEL ---
class Post(models.Model):
    """
    Blog posts using TinyMCE for rich text editing.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    featured_image = models.ImageField(upload_to='blog_featured_images/')
    
    # Rich Text Field (TinyMCE)
    content = HTMLField()
    
    # Optional short summary
    excerpt = models.CharField(max_length=300, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

# --- 5. SITE CONFIGURATION MODEL ---
class SiteConfiguration(models.Model):
    """
    Model to manage global site assets like the Hero Video and About Image.
    """
    hero_video = models.FileField(
        upload_to='site_assets/', 
        help_text="Upload the background video for the home page (MP4 recommended)."
    )
    about_image = models.ImageField(
        upload_to='site_assets/', 
        help_text="Upload the image for the 'About Me' section."
    )
    
    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Home Page Settings"