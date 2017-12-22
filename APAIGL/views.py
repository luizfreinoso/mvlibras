from django.shortcuts import render, HttpResponse
import json
from palavras.models import Palavra
# Create your views here.
def index(request):
    return render(request, 'apaigl.html')

def busca_video(request, slug):
    print "Encontrnado filme - " + slug
    try:
        print "Criando caminho"
        caminho = Palavra.objects.get(slug=slug)
        print caminho
        print "Enviando caminho"
        response_data = {'caminho': caminho.video.name,
                         'imagem': caminho.imagem.name,
                         'grupo': caminho.grupo.nome}
        print "Entregando..."
    except:
        response_data = {'caminho': '', 'erro': 'nothing'}
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")