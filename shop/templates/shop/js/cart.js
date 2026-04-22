$(document).ready(function() {
    updateCartCount();
    
    // 添加到购物车
    $('.btn-add-cart').click(function() {
        var productId = $(this).data('id');
        var quantity = 1;
        
        $.ajax({
            url: '/cart/add/',
            method: 'POST',
            data: JSON.stringify({
                'product_id': productId,
                'quantity': quantity
            }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                if (response.success) {
                    updateCartCount();
                    showNotification('已添加到购物车', 'success');
                }
            },
            error: function() {
                showNotification('添加失败', 'error');
            }
        });
    });
    
    // 更新购物车数量显示
    function updateCartCount() {
        // 简单地从服务器获取 - 可以通过API扩展
        var cartCount = localStorage.getItem('cartCount') || 0;
        $('#cartCount').text(cartCount);
    }
    
    function showNotification(message, type) {
        var notification = $('<div class="notification"></div>')
            .text(message)
            .addClass(type)
            .css({
                position: 'fixed',
                bottom: '20px',
                right: '20px',
                background: type === 'success' ? '#c6a43f' : '#8b0000',
                color: '#0a0a0a',
                padding: '1rem',
                borderRadius: '8px',
                zIndex: 9999,
                fontFamily: 'Montserrat, sans-serif'
            });
        
        $('body').append(notification);
        setTimeout(function() {
            notification.fadeOut(function() {
                $(this).remove();
            });
        }, 2000);
    }
    
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});