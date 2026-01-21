from django.db import models

class Catalog(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='catalogs/')
    thumbnail = models.ImageField(upload_to='catalogs/thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
