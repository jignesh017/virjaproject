from django.db import models
from brands.models import Brand      # import Brand

class PriceList(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="pricelists",
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pricelists/')
    thumbnail = models.ImageField(
        upload_to='pricelists/thumbnails/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['brand__name', '-created_at']

    def __str__(self):
        return self.title