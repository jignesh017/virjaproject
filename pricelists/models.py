from django.db import models

class PriceList(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pricelists/')
    thumbnail = models.ImageField(upload_to='pricelists/thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
