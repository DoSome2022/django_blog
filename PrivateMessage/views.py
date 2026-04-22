from django.shortcuts import render ,redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import PrivateMessage
from userprofile.models import UserProfile
from .forms import MessageForm
from django.contrib.auth.models import User

# Create your views here.

@login_required
def chat_room(request, friend_id):
    friend_user = get_object_or_404(User, id=friend_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)# 先別急著存進資料庫
            message.sender = request.user# 補上寄件人 (自己)
            message.receiver = friend_user# 補上收件人 (對方)
            message.save()# 真正的存檔
            return redirect('chat_room', friend_id=friend_id)# 重新整理頁面
    else:
        form = MessageForm()
    # 3. 撈取對話紀錄 (GET)
    # 邏輯：(我寄給他 OR 他寄給我)
    chats = PrivateMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=friend_user)) |
        (Q(sender=friend_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    # 4. 把對方傳給我的訊息標記為「已讀」
    # 只標記那些 "sender是對方" 且 "還沒讀" 的
    PrivateMessage.objects.filter(
        sender=friend_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    context = {
        'friend_user': friend_user,
        'chats': chats,
        'form': form,
    }

    return render(request, 'chat_room.html', context)

@login_required
def friend_list_view(request):
    # 取得當前用戶的 UserProfile
    user_profile = get_object_or_404(UserProfile, user=request.user) 
    # 取得所有好友 (假設你的 ManyToMany 欄位叫 friends)
    # 如果你的好友是另一個 Model，請在這裡調整查詢
    friends = user_profile.friends.all()

    return render(request, 'friend_list.html', {'friends': friends})