from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Post
from .forms import PostForm


class PostList(ListView):
    template_name = 'post_list.html'
    paginate_by = 20
    model = Post

    def get_queryset(self):
        posts = Post.objects.filter(
            published_date__isnull=False
        ).order_by('-published_date')
        return posts


class PostDetail(DetailView):
    template_name = 'post_detail.html'
    model = Post
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs.get(self.pk_url_kwarg))


class PostCreate(CreateView):
    template_name = 'post_new.html'
    success_url = reverse_lazy('post_list')
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostEdit(UpdateView):
    template_name = 'post_new.html'
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs.get(self.pk_url_kwarg))

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.object.id})
