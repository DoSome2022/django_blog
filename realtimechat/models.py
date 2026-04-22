from django.db import models

# Create your models here.

class PublicMessage(models.Model):
    nickname = models.CharField(max_length=100 , default="無名")

    content = models.TextField()

    image = models.ImageField(upload_to='message_images/', blank=True , null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"{self.nickname}: {self.content[:20]}..."
    
class Meta:
    # 讓最新的留言排在最上面 (排序)
    ordering = ['-created_at'] 