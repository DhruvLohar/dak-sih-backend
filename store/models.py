from django.db import models

class Collection(models.Model):
    title = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    
    collection = models.ForeignKey("store.Collection", on_delete=models.SET_NULL, related_name="products", null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    quantity_sold = models.PositiveIntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_by = models.ForeignKey("dashboard.AdminUser", on_delete=models.SET_NULL, related_name="created_products", null=True, blank=True)

    def __str__(self):
        return self.title

class UserReview(models.Model):
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey("philatelist.Philatelist", related_name="user_reviews", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Assuming a scale of 1 to 5
    review = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')  # A user can review a product only once
        ordering = ['-created_at']  # Latest reviews first

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.title} ({self.rating} Stars)"


class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey("philatelist.Philatelist", related_name="orders", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    
    transaction_details = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} ({self.status})"


class OrderLine(models.Model):
    order = models.ForeignKey("store.Order", on_delete=models.CASCADE, related_name='order_lines')
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} (Order {self.order.id})"
