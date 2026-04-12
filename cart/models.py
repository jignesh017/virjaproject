from django.db import models
from products.models import Product

class Cart(models.Model):
    # Use session_key to track carts for anonymous users
    session_key = models.CharField(max_length=40, unique=True, null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    # Submitter Details (No longer attached to Enquiry Model)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    # Reply System
    is_replied = models.BooleanField(default=False)
    reply_message = models.TextField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} - {self.session_key}"

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
