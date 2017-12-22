from django.shortcuts import HttpResponse
import json
from palavras.models import Palavra

# Create your views here.
def busca_video(request, slug, dic):
    print "Encontrnado filme -" + slug
    try:
        print "Criando caminho"
        if(int(dic) == 2):
            caminho = Palavra.objects.all().filter(slug=slug, user=request.user).last()
        
        if(int(dic) == 3):
            caminho = Palavra.objects.all().filter(slug=slug).last()
        print caminho
        print "Enviando caminho"
        response_data = {'caminho': caminho.video.name,
                         'imagem': caminho.imagem.name,
                         'grupo': caminho.grupo.nome}
        print "Entregando..." + caminho.imagem.name
    except:
        response_data = {'caminho': '', 'erro': 'nothing'}
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")