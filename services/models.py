from django.db import models

class Workshop(models.Model):
    
    banner = models.ImageField(upload_to="workshops/")
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField() # in minutes
    for_government = models.BooleanField(default=False)

    address = models.TextField()
    date = models.DateTimeField()
    
    tags = models.JSONField(default=list)
    
    price = models.PositiveIntegerField()
    # created_by ( admin user )
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.title


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