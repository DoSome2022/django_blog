from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='profile')

    codename = models.CharField(max_length=100, blank=True , verbose_name="代號")
    clearance_level = models.IntegerField(default=1 , verbose_name="權限等級")

    STATUS_CHOICES = (
        ('ACTIVE', 'Active / 現役'),
        ('MIA', 'MIA / 失蹤'),
        ('KIA', 'KIA / 陣亡'),
        ('RETIRED', 'Retired / 退休'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')

    missions_completed = models.IntegerField(default=0 , verbose_name="完成任務數")
    confirmed_kills = models.IntegerField(default=0 , verbose_name="擊殺數")
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="命中率")

    bio = models.TextField(blank=True, verbose_name="特工履歷")
    specialization = models.CharField(max_length=100, default="Survive" , verbose_name="專長")

    avatar = models.ImageField(upload_to='agent_avatars/', blank=True , null=True)
    # 'self' 代表關聯到同一個 Model (自己跟自己做朋友)
    # symmetrical=True 代表「對稱」，意思是 A 加了 B，B 自動也會有 A (雙向好友)
    # blank=True 代表可以沒有朋友 (幫QQ)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    def __str__ (self):
        return f"Agent: {self.user.username}"

# --- 自動建立 Profile 的魔法 ---
# 1. 當 User 建立時，自動建立 Profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# 2. 當 User 儲存時，順便確保 Profile 存在 (雙重保險，修復舊帳號)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # 這行是為了舊帳號：如果嘗試存取 profile 失敗，代表沒有，那就建一個
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist: # 這裡要抓 DoesNotExist 錯誤
        UserProfile.objects.create(user=instance)