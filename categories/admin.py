from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Category

@admin.register(Category)
class CategoryAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('name', 'slug', 'parent', 'is_featured', 'order')
    list_filter = ('is_featured', 'parent')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_featured')
