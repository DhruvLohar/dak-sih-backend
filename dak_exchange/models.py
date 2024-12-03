from django.db import models
from django.db import transaction

class ExchangeOrder(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey("philatelist.Philatelist", related_name="exchange_orders", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    
    transaction_details = models.JSONField(default=dict)
    product = models.ForeignKey("dak_exchange.ExchangeProduct", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} ({self.status})"

class ExchangeProduct(models.Model):
    title = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    details = models.JSONField(blank=True, null=True)
    
    # TODO: Add fields to keep track of current owner, and all the previous owners
    current_owner = models.ForeignKey("philatelist.Philatelist", on_delete=models.SET_NULL, null=True, blank=True)
    previous_owners = models.ManyToManyField("philatelist.Philatelist", related_name="previous_owners")
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    quantity_sold = models.PositiveIntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    # TODO: Add methods to transfer ownership
    def transfer_ownership(self, new_owner):        
        with transaction.atomic():
            self.previous_owners.add(self.current_owner)
            self.current_owner = new_owner
            self.save()
