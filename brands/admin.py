from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Brand

@admin.register(Brand)
class BrandAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('name', 'slug', 'is_featured')
    list_filter = ('is_featured',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_featured',)
