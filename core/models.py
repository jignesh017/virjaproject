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
    
    class Meta:
        verbose_name_plural = "Company Information"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and CompanyInfo.objects.exists():
            # If valid instance exists, don't create another
            return
        super().save(*args, **kwargs)
