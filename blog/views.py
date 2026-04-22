from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import PostForm

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    
class PostDetailView(DetailView):
    model = Post 
    template_name = 'post_detail.html'

class PostCreateview(CreateView, SuccessMessageMixin):
    model = Post
    template_name = 'post_form.html'

    form_class = PostForm
    success_message = "🎉 文章创建成功！"

class PostUpdateView(UpdateView, SuccessMessageMixin):
    model = Post
    template_name = 'post_form.html'
    form_class = PostForm
    
    success_message = "✅ 文章已更新！"


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        messages.success(self.request, "🗑️ 删除成功！")
        return super().form_valid(form)