from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ADALibras.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(?P<slug>[\w_-]+)/(?P<grupo>\d+)/(?P<dicionario>\d+)/buscarPalavra/$', views.buscarPalavra, name='buscarPalavra')
)
