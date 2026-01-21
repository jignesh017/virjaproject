from django.db import models

class Certificate(models.Model):
    title = models.CharField(max_length=255)
    image_or_pdf = models.FileField(upload_to='certificates/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
