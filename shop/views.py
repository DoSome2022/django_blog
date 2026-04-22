from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Order, OrderItem
import json

def product_list(request):
    """商品列表 - 精品店导购页面"""
    products = Product.objects.filter(available=True)
    
    # 获取情境筛选参数
    when = request.GET.get('when')
    where = request.GET.get('where')
    occasion = request.GET.get('occasion')
    
    if when:
        products = products.filter(when_to_use__icontains=when)
    if where:
        products = products.filter(where_to_use__icontains=where)
    if occasion:
        products = products.filter(occasion_to_use__icontains=occasion)
    
    context = {
        'products': products,
        'when_options': Product.objects.values_list('when_to_use', flat=True).distinct()[:10],
        'where_options': Product.objects.values_list('where_to_use', flat=True).distinct()[:10],
        'occasion_options': Product.objects.values_list('occasion_to_use', flat=True).distinct()[:10],
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, slug):
    """商品详情 - 高端推介页面"""
    product = get_object_or_404(Product, slug=slug, available=True)
    
    # 情境推介: 基于相似情境推荐其他商品
    recommendations = Product.objects.filter(
        available=True
    ).exclude(id=product.id)[:3]
    
    # 如果有限量版，优先推荐
    if product.is_limited:
        recommendations = Product.objects.filter(is_limited=True).exclude(id=product.id)[:3]
    
    context = {
        'product': product,
        'recommendations': recommendations,
    }
    return render(request, 'shop/product_detail.html', context)

@require_POST
def add_to_cart(request):
    """添加到购物车 - AJAX"""
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    
    product = get_object_or_404(Product, id=product_id)
    
    # 获取或创建购物车项
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_item, created = CartItem.objects.get_or_create(
            session_key=session_key,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    
    # 获取购物车总数
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = CartItem.objects.filter(session_key=session_key).count()
    
    return JsonResponse({'success': True, 'cart_count': cart_count})

def cart_view(request):
    """购物车页面"""
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_key=session_key) if session_key else []
    
    total = sum(item.get_total() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'shop/cart.html', context)

@require_POST
def update_cart(request, item_id):
    """更新购物车数量"""
    data = json.loads(request.body)
    quantity = int(data.get('quantity', 0))
    
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    else:
        session_key = request.session.session_key
        cart_item = get_object_or_404(CartItem, id=item_id, session_key=session_key)
    
    if quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()
    
    # 重新计算总数
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.get_total() for item in cart_items)
    
    return JsonResponse({'success': True, 'total': float(total), 'item_total': float(cart_item.product.price * quantity) if quantity > 0 else 0})

@require_POST
def checkout(request):
    """结账"""
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        user = request.user
        session_key = None
    else:
        session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_key=session_key)
        user = None
    
    if not cart_items:
        return JsonResponse({'success': False, 'error': '购物车为空'}, status=400)
    
    total = sum(item.get_total() for item in cart_items)
    
    # 创建订单
    order = Order.objects.create(
        user=user,
        session_key=session_key,
        total_amount=total,
        customer_name=data.get('customer_name', ''),
        customer_phone=data.get('customer_phone', ''),
        special_requests=data.get('special_requests', '')
    )
    
    # 创建订单项
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        # 减少库存
        item.product.stock -= item.quantity
        item.product.save()
    
    # 清空购物车
    cart_items.delete()
    
    return JsonResponse({'success': True, 'order_id': order.id})

def cart_count(request):
    """获取购物车商品数量"""
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    else:
        session_key = request.session.session_key
        if session_key:
            count = CartItem.objects.filter(session_key=session_key).count()
        else:
            count = 0
    return JsonResponse({'count': count})