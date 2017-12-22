from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import json
from palavras.models import Palavra, Grupo

# Create your views here.
def index(request):
    grupos = Grupo.objects.all().order_by('nome')
    
    return render(request, 'apalp.html', {'grupos': grupos})

def salvarVideo(request):
    print "recebendo...."
    response_data = {'palavra_pk': 'none'}
    print "data created, grupo " + request.POST['grupo']
    grupo = get_object_or_404(Grupo, pk=int(request.POST['grupo']))
    print "grupo encontrado : " + grupo.nome
    
    if(request.POST['palavra'] != "" and 'video' in request.FILES):
        print "entrou"

        palavra = Palavra.objects.create(user=request.user,
                                         nome=request.POST['palavra'],
                                         grupo=grupo,
                                         slug=request.POST['slug']
                                         )
        
        print "verificando imagem"
        if 'imagem' in request.FILES:
            palavra.imagem = request.FILES['imagem']
        print 'verificando video'
        if 'video' in request.FILES:
            request.FILES['video'].name = request.POST['slug'] + ".webm"  # renomeamos o blob
            palavra.video = request.FILES['video']
            
        palavra.save();
        
        response_data = {'palavra_pk': palavra.pk}
        
    else:
        response_data = {'erro_message': 'Para salvar deve-se gravar um video e ter uma palavra digitda!'}
        
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def buscarPalavra(request, slug):
    print 'buscando...'
    dados = list()
    response_data = {}
    palavras = Palavra.objects.all().filter(slug=slug)
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
        response_data = {'mensagem': 'nenhum item encontrado... grave agora mesmo essa palavra!'}
        
    return HttpResponse(json.dumps(response_data), content_type="application/json")