from django.contrib import admin
from django.utils.html import format_html
from .models import PortfolioItem, AdditionalImage, Testimonial, Post, SiteConfiguration

# --- Inline for Gallery Images ---
class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
    extra = 1 
    readonly_fields = ('image_preview',)

    @admin.display(description='Image Preview')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 4px;" />', 
                               obj.image.url)
        return "No Image"


# --- Portfolio Item Admin ---
@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_created', 'is_media_video_status', 'media_preview')
    list_filter = ('category', 'date_created')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AdditionalImageInline]

    # Status Column: Is Video?
    def is_media_video_status(self, obj):
        return obj.is_media_video()
    is_media_video_status.boolean = True
    is_media_video_status.short_description = 'Is Video'
    
    # Thumbnail Preview in List View
    @admin.display(description='Media Preview')
    def media_preview(self, obj):
        # Priority 1: Uploaded Video File
        if obj.video_file:
             return format_html(
                '<video width="150" height="100" controls muted style="object-fit: cover; border-radius: 8px;">'
                '<source src="{}" type="video/mp4">Video'
                '</video>', obj.video_file.url
            )
        # Priority 2: Cover Image
        elif obj.image_file:
            return format_html(
                '<img src="{}" width="150" height="100" style="object-fit: cover; border-radius: 8px;" />', 
                obj.image_file.url
            )
        # Priority 3: External Video Link
        elif obj.video_url:
            return "External Link"
            
        return "No Media"
        
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'description', 'slug')
        }),
        ('Media Content', {
            'fields': ('image_file', 'video_file', 'video_url'),
            'description': 'Upload a Video File (MP4) to play on site, OR provide an External Link. Use Image File for the cover.'
        }),
    )
    readonly_fields = ('date_created',)


# --- Testimonial Admin ---
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company', 'created_at')
    search_fields = ('client_name', 'company', 'quote')


# --- Blog Post Admin ---
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'image_preview')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

    @admin.display(description='Featured Image')
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="150" height="100" style="object-fit: cover; border-radius: 8px;" />', 
                               obj.featured_image.url)
        return "No Image"

# --- Site Config Admin ---
@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'hero_preview', 'about_preview')

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    @admin.display(description='Hero Video')
    def hero_preview(self, obj):
        if obj.hero_video:
            return "Video Uploaded"
        return "No Video"

    @admin.display(description='About Image')
    def about_preview(self, obj):
        if obj.about_image:
             return format_html('<img src="{}" width="100" style="border-radius: 4px;" />', obj.about_image.url)
        return "No Image"