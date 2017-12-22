from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ADALibras.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^grupo_palavra/$', views.grupo_palavra, name='grupo_palavra'),
    url(r'^salvarVideo/$', views.salvarVideo, name='salvarVideo')
)
