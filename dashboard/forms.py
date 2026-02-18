from django import forms
from django_summernote.widgets import SummernoteWidget
from core.models import CompanyInfo, HomePageContent, HomeFeature, SMTPSettings
from banners.models import Banner
from products.models import Product
from categories.models import Category
from brands.models import Brand
from catalogs.models import Catalog
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm


class TailwindMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.TextInput, forms.NumberInput, forms.EmailInput, forms.URLInput, forms.PasswordInput, forms.Textarea, forms.Select)):
                widget.attrs.update({
                    'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50 py-2 px-3 border'
                })
            elif isinstance(widget, (forms.FileInput, forms.ClearableFileInput)):
                 widget.attrs.update({
                    'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
                })

class CustomSetPasswordForm(TailwindMixin, SetPasswordForm):
    pass


class AdminProfileForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        }

class CustomPasswordChangeForm(TailwindMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove autofocus from old_password field
        if 'old_password' in self.fields:
            self.fields['old_password'].widget.attrs.pop('autofocus', None)

class CompanyInfoForm(TailwindMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders for specific fields
        placeholders = {
            'facebook': 'https://facebook.com/your-page',
            'twitter': 'https://twitter.com/your-handle',
            'instagram': 'https://instagram.com/your-handle',
            'linkedin': 'https://linkedin.com/company/your-company',
            'youtube': 'https://youtube.com/channel/your-channel',
            'name': 'e.g. Virja Industries',
            'address': 'Full physical address',
            'phone': '+91 98765 43210',
            'email': 'contact@example.com',
            'header_phone': 'Short number for header',
            'header_email': 'Short email for header',
            'map_embed_code': '<iframe src="..."></iframe>',
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['placeholder'] = placeholder

    class Meta:
        model = CompanyInfo
        fields = '__all__'
        widgets = {
            'about_us': SummernoteWidget(),
            'mission': SummernoteWidget(),
            'vision': SummernoteWidget(),
            'footer_description': SummernoteWidget(),
            'address': forms.Textarea(attrs={'rows': 3}),
            'map_embed_code': forms.Textarea(attrs={'rows': 3}),
        }

class HomePageContentForm(TailwindMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'hero_fallback_title': 'e.g. Welcome to Virja Industries',
            'categories_title': 'Browse Categories',
            'featured_products_title': 'Featured Products',
            'brands_title': 'Our Brands',
            'cta_title': 'Ready to get started?',
            'cta_btn_text': 'Primary Action (e.g. Shop Now)',
            'cta_btn_link': '/products/',
            'catalog_btn_text': 'Secondary Action (e.g. Contact Us)',
            'catalog_btn_link': '/contact/',
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['placeholder'] = placeholder

    class Meta:
        model = HomePageContent
        fields = '__all__'
        widgets = {
            'hero_fallback_text': SummernoteWidget(),
            'cta_text': SummernoteWidget(),
        }

class HomeFeatureForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = HomeFeature
        fields = '__all__'

class ProductForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': SummernoteWidget(),
            'specification': SummernoteWidget(),
        }
class CategoryForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'description': SummernoteWidget(),
        }

class BrandForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        widgets = {
            'description': SummernoteWidget(),
        }

class SMTPSettingsForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = SMTPSettings
        fields = '__all__'
        widgets = {
            'email_host_password': forms.PasswordInput(render_value=True),
        }

class NewsletterSendForm(TailwindMixin, forms.Form):
    subject = forms.CharField(max_length=255, required=True)
    message = forms.CharField(widget=SummernoteWidget(), required=True)

class CatalogForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = Catalog
        fields = '__all__'
        widgets = {
            'pdf_file': forms.FileInput(attrs={'accept': '.pdf'}),
        }

class BannerForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'
