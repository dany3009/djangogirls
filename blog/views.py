from django.conf import settings
from django.utils.http import is_safe_url
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login as auth_login
from braces.views import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, FormView)

from .models import Post
from .forms import PostForm, UserAuthenticationForm


class PostList(ListView):
    template_name = 'blog/post_list.html'
    paginate_by = 20
    model = Post

    def get_queryset(self):
        posts = Post.objects.filter(
            published_date__isnull=False
        ).order_by('-published_date')
        return posts


class PostDetail(DetailView):
    template_name = 'blog/post_detail.html'
    model = Post
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs.get(self.pk_url_kwarg))


class PostCreate(LoginRequiredMixin, CreateView):
    template_name = 'blog/post_new.html'
    success_url = reverse_lazy('post_list')
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    template_name = 'blog/post_edit.html'
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs.get(self.pk_url_kwarg))

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.object.id})


class UserAuthenticationView(FormView):
    form_class = UserAuthenticationForm
    template_name = 'auth/login.html'

    def get_success_url(self):
        if is_safe_url(url=self.request.POST.get('next'),
                       host=self.request.get_host()):
            return self.request.POST.get('next')
        return reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return super(UserAuthenticationView, self).form_valid(form)
