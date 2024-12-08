from django.db import models

class ForumPostImage(models.Model):
    post = models.ForeignKey("forum.ForumPost", related_name="post_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="forum/")

    def __str__(self) -> str:
        return self.post.id

class ForumPost(models.Model):
    user = models.ForeignKey(
        "philatelist.Philatelist", 
        on_delete=models.CASCADE, 
        related_name='forum_posts'
    )
    
    content = models.TextField()  # Post content (like tweet content)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    likes_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Post by {self.user.name} at {self.created_at}"


class ForumPostReply(models.Model):
    post = models.ForeignKey(
        "forum.ForumPost", 
        on_delete=models.CASCADE, related_name='replies'
    )
    user = models.ForeignKey(
        "philatelist.Philatelist", 
        on_delete=models.CASCADE, 
        related_name='post_replies'
    )
    
    content = models.TextField()  # Reply content
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Reply by {self.user.name} on {self.post.title}"