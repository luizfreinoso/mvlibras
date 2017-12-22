from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ADALibras.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^anexar/$', views.anexar, name='anexar'),
    url(r'^(?P<id>\d+)/habilitar_desabilitar/$', views.habilitar_desabilitar, name='habilitar_desabilitar'),
    url(r'^(?P<id>\d+)/excluir/$', views.excluir, name='excluir'),
)
