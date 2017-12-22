from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ADALivras_v_2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('homepage.urls', namespace='homepage')),
    
    # modulos
    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^aps/', include('AP.urls', namespace='aps')),
    url(r'^apaeld/', include('APAELD.urls', namespace='apaeld')),
    url(r'^apaigl/', include('APAIGL.urls', namespace='apaigl')),
    url(r'^apalp/', include('APALP.urls', namespace='apalp')),
    url(r'^apapsrl/', include('APAPSRL.urls', namespace='apapsrl')),
    
    # recursos
    url(r'^rbusca/', include('RBusca.urls', namespace='rbusca')),
    url(r'^rcaptura/', include('RCaptura.urls', namespace='rcaptura')),
    url(r'^rdatilologia/', include('RDatilologia.urls', namespace='rdatilologia')),
    url(r'^rinterpretador/', include('RInterpretador.urls', namespace='rinterpretador')),
    url(r'^ranexos/', include('RAnexos.urls', namespace='ranexos')),
    url(r'^rhtml/', include('RHTML.urls', namespace='rhtml')),
    url(r'^rcapturaLonga/', include('RCapturaLonga.urls', namespace='rcapturalonga')),
    url(r'^rdatilologiavisual/', include('RDatilologiaVisual.urls', namespace='rdatilologiavisual'))
)