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
    

class PDA(models.Model):
    # Personal Details
    TYPE_CHOICES = [
        ('Private', 'Private / Individual'),
        ('Dealer', 'Stamp Dealer / Shop'),
        ('Company', 'Company'),
    ]
    customer_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name_of_applicant = models.CharField(max_length=100)
    mailing_address = models.TextField()
    pin_code = models.CharField(max_length=10)
    gift_subscription_name = models.CharField(max_length=100, blank=True, null=True)
    gift_subscription_address = models.TextField(blank=True, null=True)
    
    # Order Frequency
    FREQUENCY_CHOICES = [
        ('Once a Year', 'Once a Year'),
        ('Twice a Year', 'Twice a Year'),
        ('Four Times a Year', 'Four Times a Year'),
        ('Six Times a Year', 'Six Times a Year'),
    ]
    order_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    
    # Order Details
    mint_commemorative_stamps = models.IntegerField(default=0)
    mint_commemorative_stamps_no_personality = models.IntegerField(default=0)
    mint_definitive_stamps = models.IntegerField(default=0)
    top_marginal_block_of_4 = models.IntegerField(default=0)
    bottom_marginal_block_of_4 = models.IntegerField(default=0)
    full_sheet = models.IntegerField(default=0)
    
    first_day_covers_stamped_cancelled = models.IntegerField(default=0)
    first_day_covers_no_personality = models.IntegerField(default=0)
    first_day_covers_blank = models.IntegerField(default=0)
    
    information_brochure_stamped_cancelled = models.IntegerField(default=0)
    information_brochure_blank = models.IntegerField(default=0)
    
    annual_stamp_pack = models.IntegerField(default=0)
    special_annual_stamp_pack_personalities = models.IntegerField(default=0)
    childrens_special_stamp_pack = models.IntegerField(default=0)
    special_collectors_stamp_pack = models.IntegerField(default=0)
    first_day_cover_pack_thematic = models.IntegerField(default=0)
    
    postal_stationery = models.IntegerField(default=0)
    mini_sheets = models.IntegerField(default=0)
    other_items = models.TextField(blank=True, null=True)
    
    # For Office Use
    date_of_application = models.DateField(auto_now_add=True)
    signature_of_applicant = models.ImageField(upload_to='signatures/')
    
    def __str__(self):
        return f"{self.name_of_applicant} - {self.date_of_application}"
