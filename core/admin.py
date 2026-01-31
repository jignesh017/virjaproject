from django.contrib import admin
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import CompanyInfo, HomePageContent, HomeFeature

@admin.register(CompanyInfo)
class CompanyInfoAdmin(SummernoteModelAdmin):
    summernote_fields = ('about_us', 'mission', 'vision', 'footer_description')
    fieldsets = (
        ('General Info', {
            'fields': ('name', 'logo', 'favicon', 'address', 'map_embed_code')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'header_phone', 'header_email')
        }),
        ('Content', {
            'fields': ('about_us', 'mission', 'vision', 'footer_description')
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'youtube')
        }),
    )

    def has_add_permission(self, request):
        if CompanyInfo.objects.exists():
            return False
        return True

@admin.register(HomePageContent)
class HomePageContentAdmin(SummernoteModelAdmin):
    summernote_fields = ('hero_fallback_text', 'cta_text')
    fieldsets = (
        ('Hero Section (Fallback)', {
            'fields': ('hero_fallback_title', 'hero_fallback_text')
        }),
        ('Features Section', {
            'fields': ('features_section_enabled',)
        }),
        ('Section Titles', {
            'fields': ('categories_title', 'categories_subtitle', 'featured_products_title', 'featured_products_subtitle', 'brands_title')
        }),
        ('Call to Action', {
            'fields': ('cta_title', 'cta_text', 'cta_btn_text', 'cta_btn_link', 'catalog_btn_text', 'catalog_btn_link', 'cta_background_image')
        }),
    )

    def has_add_permission(self, request):
        if HomePageContent.objects.exists():
            return False
        return True

@admin.register(HomeFeature)
class HomeFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'order')
    list_editable = ('order',)
    search_fields = ('title',)
