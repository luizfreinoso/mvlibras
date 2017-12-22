from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ADALibras.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^salvarVideo/$', views.salvarVideo, name='salvarVideo'),
    url(r'^(?P<slug>[\w_-]+)/buscarPalavra/$', views.buscarPalavra, name='buscarPalavra'),
)
