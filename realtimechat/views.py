from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import PublicMessage
from .forms import MessageForm

# Create your views here.


class MessageCreateView(CreateView):
    form_class = MessageForm
    model = PublicMessage
    template_name = 'message_form.html'
    # 成功後重新導向回同一頁 (這樣才能看到剛發的留言)
    success_url = reverse_lazy('realtime_chat')

    # 關鍵：覆寫這個方法來加入「留言列表」
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 把所有留言抓出來，塞進 context 裡
        context['messages'] = PublicMessage.objects.all() 
        return context