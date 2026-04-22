from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    """商品类别 - 武器类型"""
    name = models.CharField(max_length=50, verbose_name="類別名稱")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name="類別描述")
    
    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = "商品类别"
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    """商品模型 - 高级军火"""
    # 情境式导购字段
    name = models.CharField(max_length=200, verbose_name="商品名稱")
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    # 西餐厅/精品店风格的描述
    tagline = models.CharField(max_length=200, blank=True, verbose_name="標語",
                               help_text="例：'犹如神户牛排的完美熟度'")
    description = models.TextField(verbose_name="商品描述")
    
    # 关键: 情境导购字段
    when_to_use = models.CharField(max_length=200, verbose_name="何時使用",
                                   help_text="例：'当您需要在三秒内解决六名敌人'")
    where_to_use = models.CharField(max_length=200, verbose_name="何地使用",
                                    help_text="例：'罗马地下墓穴，或纽约地铁站'")
    occasion_to_use = models.CharField(max_length=200, verbose_name="何种场合",
                                       help_text="例：'背叛之后的复仇，或契约完成后的庆功'")
    
    # 价格与库存
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    stock = models.IntegerField(default=0, verbose_name="库存")
    available = models.BooleanField(default=True, verbose_name="是否上架")
    
    # 精美图片
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="商品图片")
    
    # 高级定制选项
    is_limited = models.BooleanField(default=False, verbose_name="限量版")
    limited_edition_number = models.IntegerField(blank=True, null=True, verbose_name="限量编号")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "商品"
        verbose_name_plural = "商品管理"
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class CartItem(models.Model):
    """购物车项"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def get_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.name}"
    
class Order(models.Model):
    """订单"""
    STATUS_CHOICES = [
        ('pending', '等待处理'),
        ('paid', '已付款'),
        ('shipped', '已发货'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # 客户信息
    customer_name = models.CharField(max_length=100, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    special_requests = models.TextField(blank=True, verbose_name="特殊要求",
                                        help_text="例如：'请用黑市专用的包装'")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "订单"
        verbose_name_plural = "訂單管理"
    
    def __str__(self):
        return f"Order #{self.id} - {self.status}"

class OrderItem(models.Model):
    """订单明细"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_total(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"