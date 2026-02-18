from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from core.models import CompanyInfo, HomePageContent, HomeFeature, SMTPSettings, NewsletterSubscriber
from banners.models import Banner
from products.models import Product
from categories.models import Category
from brands.models import Brand
from enquiries.models import Enquiry
from .forms import (
    CompanyInfoForm, HomePageContentForm, HomeFeatureForm, 
    ProductForm, CategoryForm, BrandForm, SMTPSettingsForm,
    NewsletterSendForm, CatalogForm, AdminProfileForm, CustomPasswordChangeForm,
    BannerForm
)
from catalogs.models import Catalog
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from core.utils import send_custom_email

def admin_required(user):
    return user.is_superuser

def login_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('dashboard:home')
                else:
                    messages.error(request, "You are not authorized to access this panel.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'dashboard/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('dashboard:login')

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def home(request):
    stats = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_catalogs': Catalog.objects.count(),
        'newsletter_count': NewsletterSubscriber.objects.count(),
        'total_brands': Brand.objects.count(),
        'total_banners': Banner.objects.count(),
        'new_enquiries': Enquiry.objects.filter(is_read=False).count(),
    }
    return render(request, 'dashboard/home.html', {'stats': stats})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def site_settings_view(request):
    company_info = CompanyInfo.objects.first()
    if request.method == 'POST':
        form = CompanyInfoForm(request.POST, request.FILES, instance=company_info)
        if form.is_valid():
            form.save()
            messages.success(request, "Site settings updated successfully.")
            return redirect('dashboard:site_settings')
    else:
        form = CompanyInfoForm(instance=company_info)
    
    return render(request, 'dashboard/settings/site_info.html', {'form': form})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def home_content_view(request):
    home_content = HomePageContent.objects.first()
    # Handle Features Formset or similar if needed, but for now just the main content
    
    if request.method == 'POST':
        form = HomePageContentForm(request.POST, request.FILES, instance=home_content)
        if form.is_valid():
            form.save()
            messages.success(request, "Home page content updated successfully.")
            return redirect('dashboard:home_content')
    else:
        form = HomePageContentForm(instance=home_content)
        
    return render(request, 'dashboard/settings/home_content.html', {'form': form})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def smtp_settings_view(request):
    smtp_settings = SMTPSettings.objects.first()
    if request.method == 'POST':
        form = SMTPSettingsForm(request.POST, instance=smtp_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "SMTP settings updated successfully.")
            return redirect('dashboard:smtp_settings')
    else:
        form = SMTPSettingsForm(instance=smtp_settings)
        
    return render(request, 'dashboard/settings/smtp_settings.html', {'form': form})

# Catalog Views

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def product_list(request):
    products = Product.objects.all().select_related('category', 'brand').order_by('-created_at')
    return render(request, 'dashboard/catalog/product_list.html', {'products': products})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully.")
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()
    return render(request, 'dashboard/catalog/product_form.html', {'form': form, 'title': 'Add Product'})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def product_edit(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/catalog/product_form.html', {'form': form, 'title': 'Edit Product'})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('dashboard:product_list')
    return render(request, 'dashboard/catalog/product_confirm_delete.html', {'product': product})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def category_list(request):
    categories = Category.objects.all().order_by('order', 'name')
    return render(request, 'dashboard/catalog/category_list.html', {'categories': categories})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def brand_list(request):
    brands = Brand.objects.all().order_by('name')
    return render(request, 'dashboard/catalog/brand_list.html', {'brands': brands})

# Category CRUD
@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/catalog/category_form.html', {'form': form, 'title': 'Add Category'})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def category_edit(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/catalog/category_form.html', {'form': form, 'title': 'Edit Category'})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def category_delete(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/catalog/category_confirm_delete.html', {'item': category, 'type': 'Category', 'cancel_url': 'dashboard:category_list'})

# Brand CRUD
@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def brand_create(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Brand created successfully.")
            return redirect('dashboard:brand_list')
    else:
        form = BrandForm()
    return render(request, 'dashboard/catalog/brand_form.html', {'form': form, 'title': 'Add Brand'})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def brand_edit(request, pk):
    brand = Brand.objects.get(pk=pk)
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, "Brand updated successfully.")
            return redirect('dashboard:brand_list')
    else:
        form = BrandForm(instance=brand)
    return render(request, 'dashboard/catalog/brand_form.html', {'form': form, 'title': 'Edit Brand'})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def brand_delete(request, pk):
    brand = Brand.objects.get(pk=pk)
    if request.method == 'POST':
        brand.delete()
        messages.success(request, "Brand deleted successfully.")
        return redirect('dashboard:brand_list')
    return render(request, 'dashboard/catalog/brand_confirm_delete.html', {'item': brand, 'type': 'Brand', 'cancel_url': 'dashboard:brand_list'})

# Enquiry Management
@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def enquiry_list(request):
    enquiries = Enquiry.objects.all().order_by('-created_at')
    return render(request, 'dashboard/enquiries/list.html', {'enquiries': enquiries})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def enquiry_detail(request, pk):
    enquiry = Enquiry.objects.get(pk=pk)
    
    # Mark as read
    if not enquiry.is_read:
        enquiry.is_read = True
        enquiry.save()

    if request.method == 'POST':
        reply_message = request.POST.get('reply_message')
        if reply_message:
            enquiry.reply_message = reply_message
            enquiry.is_replied = True
            enquiry.replied_at = timezone.now()
            enquiry.save()

            # Send Email Reply (Simulated)
            subject = f"Re: Your Enquiry to Virja Industries"
            msg_body = f"Hello {enquiry.name},\n\nThank you for your enquiry. Your Message:\n\n\"{enquiry.message}\"\n\nVirja Automation Reply:\n\n{reply_message}\n\nBest Regards,\nVirja Industries Team"
            
            html_content = render_to_string('dashboard/emails/reply_email.html', {
                'enquiry': enquiry,
                'reply_message': reply_message
            })

            if send_custom_email(subject, msg_body, [enquiry.email], html_message=html_content):
                messages.success(request, f"Reply sent successfully to {enquiry.email}")
            else:
                messages.warning(request, f"Reply saved to database, but failed to send email to {enquiry.email}. Please check SMTP settings.")
                
            return redirect('dashboard:enquiry_list')

    return render(request, 'dashboard/enquiries/detail.html', {'enquiry': enquiry})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def enquiry_delete(request, pk):
    enquiry = Enquiry.objects.get(pk=pk)
    if request.method == 'POST':
        enquiry.delete()
        messages.success(request, "Enquiry deleted successfully.")
        return redirect('dashboard:enquiry_list')
    return render(request, 'dashboard/catalog/category_confirm_delete.html', {
        'item': enquiry, 
        'type': 'Enquiry', 
        'cancel_url': 'dashboard:enquiry_list'
    })

# Newsletter Management
@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def newsletter_list(request):
    subscribers = NewsletterSubscriber.objects.all().order_by('-subscribed_at')
    return render(request, 'dashboard/newsletter/list.html', {'subscribers': subscribers})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def newsletter_send(request):
    if request.method == 'POST':
        form = NewsletterSendForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            subscribers = NewsletterSubscriber.objects.filter(is_active=True)
            recipient_list = [sub.email for sub in subscribers]
            
            if not recipient_list:
                messages.warning(request, "No active subscribers found.")
                return redirect('dashboard:newsletter_list')

            # Send emails in bulk (bcc) or individually
            # For simplicity, sending individually or handling bcc depends on email provider limits
            # Here we send as BCC to protect privacy if supported, or individual loop
            
            success_count = 0
            for email in recipient_list:
                 # Minimal HTML wrapper for promo email
                html_content = render_to_string('dashboard/emails/promo_email.html', {
                    'message': message,
                    'subject': subject
                })
                if send_custom_email(subject, message, [email], html_message=html_content):
                    success_count += 1
            
            messages.success(request, f"Promotional email sent to {success_count} subscribers.")
            return redirect('dashboard:newsletter_list')
    else:
        form = NewsletterSendForm()
    
    return render(request, 'dashboard/newsletter/send.html', {'form': form})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def newsletter_delete(request, pk):
    subscriber = NewsletterSubscriber.objects.get(pk=pk)
    if request.method == 'POST':
        subscriber.delete()
        messages.success(request, "Subscriber removed successfully.")
        return redirect('dashboard:newsletter_list')
    return render(request, 'dashboard/catalog/category_confirm_delete.html', {
        'item': subscriber,
        'type': 'Subscriber',
        'cancel_url': 'dashboard:newsletter_list'
    })

# Catalog PDF Management
@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def catalog_list_view(request):
    catalogs = Catalog.objects.all().order_by('-created_at')
    return render(request, 'dashboard/catalogs/list.html', {'catalogs': catalogs})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def catalog_add(request):
    if request.method == 'POST':
        form = CatalogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Catalog uploaded successfully.")
            return redirect('dashboard:catalog_list')
    else:
        form = CatalogForm()
    return render(request, 'dashboard/catalogs/form.html', {'form': form, 'title': 'Upload Catalog'})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def catalog_edit(request, pk):
    catalog = Catalog.objects.get(pk=pk)
    if request.method == 'POST':
        form = CatalogForm(request.POST, request.FILES, instance=catalog)
        if form.is_valid():
            form.save()
            messages.success(request, "Catalog updated successfully.")
            return redirect('dashboard:catalog_list')
    else:
        form = CatalogForm(instance=catalog)
    return render(request, 'dashboard/catalogs/form.html', {'form': form, 'title': 'Edit Catalog'})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def catalog_delete(request, pk):
    catalog = Catalog.objects.get(pk=pk)
    if request.method == 'POST':
        catalog.delete()
        messages.success(request, "Catalog deleted successfully.")
        return redirect('dashboard:catalog_list')
    return render(request, 'dashboard/catalog/category_confirm_delete.html', {
        'item': catalog,
        'type': 'Catalog',
        'cancel_url': 'dashboard:catalog_list'
    })

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def admin_profile(request):
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = AdminProfileForm(request.POST, instance=request.user)
            password_form = CustomPasswordChangeForm(request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('dashboard:admin_profile')
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            profile_form = AdminProfileForm(instance=request.user)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('dashboard:admin_profile')
    else:
        profile_form = AdminProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
        
    return render(request, 'dashboard/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })

# Banner Management
@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def banner_list(request):
    banners = Banner.objects.all().order_by('order')
    return render(request, 'dashboard/banners/list.html', {'banners': banners})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def banner_create(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Banner created successfully.")
            return redirect('dashboard:banner_list')
    else:
        form = BannerForm()
    return render(request, 'dashboard/banners/form.html', {'form': form, 'title': 'Add Banner'})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def banner_edit(request, pk):
    banner = Banner.objects.get(pk=pk)
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            messages.success(request, "Banner updated successfully.")
            return redirect('dashboard:banner_list')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'dashboard/banners/form.html', {'form': form, 'title': 'Edit Banner'})

@login_required(login_url='dashboard:login')
@user_passes_test(admin_required, login_url='dashboard:login')
def banner_delete(request, pk):
    banner = Banner.objects.get(pk=pk)
    if request.method == 'POST':
        banner.delete()
        messages.success(request, "Banner deleted successfully.")
        return redirect('dashboard:banner_list')
    return render(request, 'dashboard/catalog/category_confirm_delete.html', {
        'item': banner,
        'type': 'Banner',
        'cancel_url': 'dashboard:banner_list'
    })
