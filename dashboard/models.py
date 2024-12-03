from django.db import models
from philatelist.models import Philatelist

class PostalOffice(models.Model):
    alias = models.TextField(max_length=255)
    main_office = models.TextField(max_length=100)
    sub_division = models.TextField(max_length=100)
    postal_code = models.TextField(max_length=10)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.alias} ({self.main_office})"


class AdminUser(Philatelist):
    postal_office = models.ForeignKey(PostalOffice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.postal_office})"
