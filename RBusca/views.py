from django.shortcuts import HttpResponse, get_object_or_404
from palavras.models import Palavra, Grupo
import json

# Create your views here.
def buscarPalavra(request, slug, grupo, dicionario):
    print 'buscando...'
    dados = list()
    response_data = {}
    palavras = {}
    
    if int(grupo) != 0:
        bgrupo = get_object_or_404(Grupo, pk=int(grupo))
        if int(dicionario) == 0 or int(dicionario) == 3: #TODOS, grupo
            palavras = Palavra.objects.all().filter(slug__contains=slug, grupo=bgrupo)
        if int(dicionario) == 2: #pessoal
            palavras = Palavra.objects.all().filter(slug__contains=slug, grupo=bgrupo, user=request.user)
    else:
        if int(dicionario) == 0 or int(dicionario) == 3: #TODOS, grupo
            palavras = Palavra.objects.all().filter(slug__contains=slug)
        if int(dicionario) == 2: #pessoal
            palavras = Palavra.objects.all().filter(slug__contains=slug, user=request.user)
    
    print palavras.count()
    
    if (palavras.count() > 0):
        print 'Enviando...'
        # montamos um grande string com os caminhos
        for palavra in palavras:
            dados.append({'caminho': palavra.video.name})
        response_data['caminhos'] = dados
        print response_data
    else:
        print 'Nenuhma evidencia..'
        response_data = {'mensagem': 'nenhum item local ou pessoal encontrado... !'}
        
    return HttpResponse(json.dumps(response_data), content_type="application/json")