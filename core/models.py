from django.db import models

class CompanyInfo(models.Model):
    name = models.CharField(max_length=255, default="Virja Industries")
    about_us = models.TextField(help_text="HTML allowed")
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    map_embed_code = models.TextField(help_text="Google Maps Embed Iframe HTML", blank=True)
    
    # New Fields
    logo = models.ImageField(upload_to='company_info/', null=True, blank=True)
    favicon = models.ImageField(upload_to='company_info/', null=True, blank=True)
    header_phone = models.CharField(max_length=50, blank=True, help_text="Phone number for header (if different)")
    header_email = models.EmailField(blank=True, help_text="Email for header (if different)")
    footer_description = models.TextField(blank=True, help_text="Short description for footer")
    
    # Social Media
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    whatsapp_link = models.URLField(blank=True, help_text="Direct WhatsApp link (e.g., https://wa.me/911234567890)")
    
    class Meta:
        verbose_name_plural = "Company Information"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and CompanyInfo.objects.exists():
            # If valid instance exists, don't create another
            return
        super().save(*args, **kwargs)

class HomePageContent(models.Model):
    # Hero Section Fallback (if no banners)
    hero_fallback_title = models.CharField(max_length=255, default="Industrial Excellence")
    hero_fallback_text = models.TextField(default="Premium tools, machinery, and safety equipment for professional applications.")
    
    # Features Section
    features_section_enabled = models.BooleanField(default=True)
    
    # Section Titles
    categories_title = models.CharField(max_length=255, default="Browse Categories")
    categories_subtitle = models.CharField(max_length=255, default="Our Collection")
    
    featured_products_title = models.CharField(max_length=255, default="Featured Products")
    featured_products_subtitle = models.CharField(max_length=255, default="Top Picks")
    
    brands_title = models.CharField(max_length=255, default="Trusted By Industry Leaders")
    
    # CTA Section
    cta_title = models.CharField(max_length=255, default="Ready to Optimize Your Production?")
    cta_text = models.TextField(default="Get custom quotes, technical specifications, and bulk pricing for all your industrial needs.")
    cta_btn_text = models.CharField(max_length=50, default="Request a Quote")
    cta_btn_link = models.CharField(max_length=255, default="/contact/")
    catalog_btn_text = models.CharField(max_length=50, default="Download Catalog")
    catalog_btn_link = models.CharField(max_length=255, default="/catalogs/")
    cta_background_image = models.ImageField(upload_to='home_content/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Home Page Content"

    def __str__(self):
        return "Home Page Content"

    def save(self, *args, **kwargs):
        if not self.pk and HomePageContent.objects.exists():
            return
        super().save(*args, **kwargs)

class HomeFeature(models.Model):
    icon = models.CharField(max_length=50, help_text="FontAwesome class (e.g., fas fa-shipping-fast)")
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class SMTPSettings(models.Model):
    email_host = models.CharField(max_length=255, default="smtp.gmail.com")
    email_port = models.IntegerField(default=587)
    email_host_user = models.CharField(max_length=255, blank=True)
    email_host_password = models.CharField(max_length=255, blank=True)
    email_use_tls = models.BooleanField(default=True)
    email_use_ssl = models.BooleanField(default=False)
    default_from_email = models.EmailField(default="noreply@example.com")

    class Meta:
        verbose_name_plural = "SMTP Settings"

    def __str__(self):
        return f"SMTP: {self.email_host}"

    def save(self, *args, **kwargs):
        if not self.pk and SMTPSettings.objects.exists():
            return
        super().save(*args, **kwargs)

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
