from django.contrib import admin
from palavras.models import Palavra, palavra_avaliacao, Grupo

# Register your models here.
class GrupoAdmin(admin.ModelAdmin):
    fields = ['nome', 'user','pub_date']
    list_display = ('nome','user','pub_date')

class PalavraAdmin(admin.ModelAdmin):
    fields = ['nome', 'slug','grupo','user', 'data_criacao']
    list_display = ('nome', 'slug', 'grupo', 'user', 'data_criacao')

admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Palavra, PalavraAdmin)