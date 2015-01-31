from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

from blog.views import UserAuthenticationView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', UserAuthenticationView.as_view(), name='auth_login'),
    url(r'^logout/$', auth_views.logout,
        {'next_page': reverse_lazy(settings.LOGOUT_REDIRECT_URL)},
        name='auth_logout'),

    url(r'^', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
