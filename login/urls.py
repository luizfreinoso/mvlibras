from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()
import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MusicalHaking.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='login'),
    url(r'^registrar/$', views.registrar, name='registrar'),
    url(r'^logar/$', views.logar, name='logar'),
    url(r'^logout/$', views.logout, name='logout'),
)
