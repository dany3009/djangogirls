from django.conf.urls import patterns, include, url
from .views import PostList, PostDetail, PostCreate, PostEdit


urlpatterns = patterns('',
    url(r'^$', PostList.as_view(), name='post_list'),
    url(r'^post/(?P<post_id>[0-9]+)/$', PostDetail.as_view(), name='post_detail'),
    url(r'^post/new/$', PostCreate.as_view(), name='post_new'),
    url(r'^post/(?P<post_id>[0-9]+)/edit/$', PostEdit.as_view(), name='post_edit'),
)