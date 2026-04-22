from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        #驗證成功
        if form.is_valid(): 
            form.save()# 存入資料庫，自動處理密碼加密
            username = form.cleaned_data.get('username')
            messages.success(request , f'🎉 账号 {username} 创建成功！')
            return redirect('login')# 註冊成功跳轉去登入頁
    else:
            # 如果是 GET 請求，就給一個空表單
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})