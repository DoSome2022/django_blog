from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, CartItem, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available', 'is_limited', 'image_preview')
    list_filter = ('category', 'available', 'is_limited', 'created_at')
    search_fields = ('name', 'description', 'when_to_use', 'where_to_use', 'occasion_to_use')
    list_editable = ('price', 'stock', 'available')
    
    fieldsets = (
        ('基础信息', {
            'fields': ('name', 'slug', 'category', 'tagline', 'description', 'image')
        }),
        ('情境导购 (John Wick 风格)', {
            'fields': ('when_to_use', 'where_to_use', 'occasion_to_use'),
            'classes': ('wide',),
            'description': '这些信息将展示在商品页面，帮助客户像挑选高级定制西装一样选择军火'
        }),
        ('价格与库存', {
            'fields': ('price', 'stock', 'available')
        }),
        ('限量版信息', {
            'fields': ('is_limited', 'limited_edition_number'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 4px;" />', obj.image.url)
        return "无图片"
    image_preview.short_description = "预览"
    
    actions = ['mark_as_unavailable']
    
    def mark_as_unavailable(self, request, queryset):
        queryset.update(available=False)
    mark_as_unavailable.short_description = "标记为下架"

# 将 OrderItemInline 移到 OrderAdmin 之前
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('product', 'quantity', 'price')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'created_at', 'total_amount', 'status', 'special_requests_summary')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'special_requests')
    list_editable = ('status',)
    
    readonly_fields = ('total_amount', 'created_at')
    
    fieldsets = (
        ('订单信息', {
            'fields': ('user', 'session_key', 'status', 'created_at')
        }),
        ('客户信息', {
            'fields': ('customer_name', 'customer_phone', 'special_requests')
        }),
        ('金额', {
            'fields': ('total_amount',)
        }),
    )
    
    inlines = [OrderItemInline]
    
    def special_requests_summary(self, obj):
        return obj.special_requests[:50] + "..." if len(obj.special_requests) > 50 else obj.special_requests
    special_requests_summary.short_description = "特殊要求"

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)