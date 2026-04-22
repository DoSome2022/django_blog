from django.db import models
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100 , verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="更新时间")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={"pk":self.pk})
