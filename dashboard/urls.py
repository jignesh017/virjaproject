from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .forms import CustomSetPasswordForm

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/site/', views.site_settings_view, name='site_settings'),
    path('settings/home/', views.home_content_view, name='home_content'),
    path('settings/smtp/', views.smtp_settings_view, name='smtp_settings'),
    path('settings/smtp/', views.smtp_settings_view, name='smtp_settings'),
    path('profile/', views.admin_profile, name='admin_profile'),
    
    # Password Reset
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='dashboard/password_reset.html',
             email_template_name='dashboard/password_reset_email.html',
             subject_template_name='dashboard/password_reset_subject.txt',
             success_url='/dashboard/password_reset/done/'
         ), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='dashboard/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='dashboard/password_reset_confirm.html',
             success_url='/dashboard/reset/done/',
             form_class=CustomSetPasswordForm
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='dashboard/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    
    # Catalog - Products
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Catalog - Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Catalog - Brands
    path('brands/', views.brand_list, name='brand_list'),
    path('brands/add/', views.brand_create, name='brand_create'),
    path('brands/<int:pk>/edit/', views.brand_edit, name='brand_edit'),
    path('brands/<int:pk>/delete/', views.brand_delete, name='brand_delete'),

    # Enquiries
    path('enquiries/', views.enquiry_list, name='enquiry_list'),
    path('enquiries/export/', views.enquiries_export, name='enquiries_export'),
    path('enquiries/<int:pk>/', views.enquiry_detail, name='enquiry_detail'),
    path('enquiries/<int:pk>/delete/', views.enquiry_delete, name='enquiry_delete'),

    # Newsletter
    path('newsletter/', views.newsletter_list, name='newsletter_list'),
    path('newsletter/export/', views.newsletter_export, name='export_newsletter_subscribers'),
    path('newsletter/send/', views.newsletter_send, name='newsletter_send'),
    path('newsletter/<int:pk>/delete/', views.newsletter_delete, name='newsletter_delete'),
    # Catalog PDFs
    path('catalogs/', views.catalog_list_view, name='catalog_list'),
    path('catalogs/add/', views.catalog_add, name='catalog_add'),
    path('catalogs/<int:pk>/edit/', views.catalog_edit, name='catalog_edit'),
    path('catalogs/<int:pk>/delete/', views.catalog_delete, name='catalog_delete'),

    # Hero Banners
    path('banners/', views.banner_list, name='banner_list'),
    path('banners/add/', views.banner_create, name='banner_create'),
    path('banners/<int:pk>/edit/', views.banner_edit, name='banner_edit'),
    path('banners/<int:pk>/delete/', views.banner_delete, name='banner_delete'),

    # Price Lists
    path('pricelists/', views.pricelist_list_view, name='pricelist_list'),
    path('pricelists/add/', views.pricelist_add, name='pricelist_add'),
    path('pricelists/<int:pk>/edit/', views.pricelist_edit, name='pricelist_edit'),
    path('pricelists/<int:pk>/delete/', views.pricelist_delete, name='pricelist_delete'),

    # Certificates
    path('certificates-admin/', views.certificate_list_view, name='certificate_list'),
    path('certificates-admin/add/', views.certificate_add, name='certificate_add'),
    path('certificates-admin/<int:pk>/edit/', views.certificate_edit, name='certificate_edit'),
    path('certificates-admin/<int:pk>/delete/', views.certificate_delete, name='certificate_delete'),
]
