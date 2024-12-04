from django.db import models
from tinymce.models import HTMLField

class Blog(models.Model):
        
    slug = models.SlugField(default="", max_length=200)
    image = models.ImageField(upload_to="blogs/", null=True, blank=True)

    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    read_time = models.PositiveIntegerField(default=0)

    content = HTMLField(null=True, blank=True)
    
    user = models.ForeignKey("philatelist.Philatelist", related_name='blogs', on_delete=models.PROTECT)
    
    class Meta:
        ordering = ['-published_date']  

    def __str__(self) -> str:
        return self.slug

class Notification(models.Model):

    user = models.ForeignKey("philatelist.Philatelist", related_name='all_notifications', on_delete=models.PROTECT)
    
    title = models.CharField(max_length=250)
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.user.name)
    
class Announcement(models.Model):

    title = models.CharField(max_length=250)
    body = models.TextField()
    
    attachment = models.ImageField(upload_to="announcements/", null=True, blank=True)

    # announced_by = models.ForeignKey(to="dashboard.AdminUser", related_name="announcements")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    
    
class Catalog(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to="catalog/")
    
    coining_date = models.DateField()
    backstory = models.TextField()
    quantity_produced = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title

