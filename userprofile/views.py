# CRUD 用CBV ,複習的function 就用FBV

from django.shortcuts import render , redirect , get_object_or_404
from django.views.generic import DetailView , ListView ,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth import get_user_model 
from .models import UserProfile 
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AddFriendForm

User = get_user_model()

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user' 

    def get_object(self):
        user = self.request.user
        
        # --- 終極修正：直接使用 get_or_create ---
        # 這行指令會去資料庫找，找不到就自動建立，保證 profile 一定存在
        UserProfile.objects.get_or_create(user=user)
        
        # 為了保險起見，我們讓 user 重新從資料庫加載一次
        # 這樣可以清除 Django 的內部快取，確保 user.profile 是最新的
        user.refresh_from_db()
        
        return user

class UserProfileUpdateView(LoginRequiredMixin, UpdateView , SuccessMessageMixin):
    model = UserProfile
    template_name = 'user_profile_edit.html'
    context_object_name = 'profile'
    
    fields = ['status', 'avatar' ,'codename']
    success_message = "✅ 資料庫已更新！"    

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'pk': self.request.user.pk})
    def get_object(self, queryset=None):
        
        return UserProfile.objects.get_or_create(user=self.request.user)[0]
            
class UserListView(ListView):
    model = UserProfile
    template_name = 'user_list.html'
    context_object_name = 'users'
    paginate_by = 50

    def get_queryset(self):
        return UserProfile.objects.all().order_by('id')
    
@login_required
def add_friend_view(request):
    my_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = AddFriendForm(request.POST)
        if form.is_valid():
            target_id = form.cleaned_data('target_id')

            if target_id == request.user.id:
                messages.error(request, '不能加自己為好友')
            else:
                try:
                    target_profile =  UserProfile.objects.get(user__id=target_id)

                    if target_profile in my_profile.friends.all():
                        messages.error(request, f"特工 {target_profile.codename} 已經在您的名單中。")
                    else:
                        # === 關鍵動作：加好友 ===
                        # 因為我們在 model 設定了 symmetrical=True
                        # 所以只要加一邊，另一邊也會自動加上
                        my_profile.friends.add(target_profile)
                        messages.success(request, f"成功與特工 {target_profile.codename} 建立連線。")
                
                except UserProfile.DoesNotExist:
                    messages.error(request, "錯誤：找不到該 ID 的特工。")

            return redirect('add_friend') # 重整頁面
    
    else:
        form = AddFriendForm()

    # 取得我的好友列表 (用於顯示在下方)
    friend_list = my_profile.friends.all()

    context = {
        'form': form,
        'friend_list': friend_list
    }
    return render(request, 'user_add_fd.html', context)


