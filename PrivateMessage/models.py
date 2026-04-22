from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PrivateMessage(models.Model):
    # 誰寄的 (Sender)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    # 寄給誰 (Receiver)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    # 講了什麼 (Content)
    content = models.TextField()
    # 什麼時候講的 (Timestamp)
    timestamp = models.DateTimeField(auto_now_add=True)
    # 對方讀了嗎？ (Is Read) - 做紅點通知用
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-timestamp',)# 依照時間排序
    
def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"