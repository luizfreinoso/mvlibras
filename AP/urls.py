from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ADALibras.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>\d+)/ap/$', views.ap, name='ap'),
    url(r'^(?P<id>\d+)/(?P<ordem>\d+)/apordem/$', views.apordem, name='apordem'),
    url(r'^criarAP/$', views.criar, name='criarAP'),
    url(r'^criarNovaAP/$', views.criarNovaAP, name='criarNovaAP'),
    url(r'^(?P<id>\d+)/removerAP/$', views.removerAP, name='removerAP'),
    url(r'^(?P<id>\d+)/editarAP/$', views.editarAP, name='editarAP'),
    url(r'^(?P<id>\d+)/SalvarAtualizacaoAP/$', views.SalvarAtualizacaoAP, name='SalvarAtualizacaoAP'),
    url(r'^(?P<id>\d+)/configurarAP/$', views.configurarAP, name='configurarAP'),
    url(r'^(?P<id>\d+)/duplicarAP/$', views.duplicar, name='duplicarAP'),
    url(r'^(?P<id>\d+)/(?P<ordem>\d+)/salvarConfiguracaoAP/$', views.salvarConfiguracaoAP, name='salvarConfiguracaoAP'),
    url(r'^(?P<id>\d+)/salvarLog/$', views.salvarLog, name='salvarLog')
)
