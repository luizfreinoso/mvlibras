from django.shortcuts import get_object_or_404,HttpResponse
import json
from palavras.models import Grupo, Palavra
from AP.models import APDados, APListaRecursos

# Create your views here.
def salvarVideo(request):
    print "recebendo...." 
    response_data = {'palavra_pk': 'none'}
    print 'grupo...'
    print "data created, grupo " + request.POST['RCapturagrupo']
    grupo = get_object_or_404(Grupo, pk=int(request.POST['RCapturagrupo']))
    print "grupo encontrado : " + grupo.nome
    
    if(request.POST['RCapturapalavra'] != "" and 'video' in request.FILES):
        print "entrou"

        palavra = Palavra.objects.create(user=request.user,
                                         nome=request.POST['RCapturapalavra'],
                                         grupo=grupo,
                                         slug=request.POST['RCapturaslug']
                                         )
        
        print "verificando imagem"
        if 'RCapturaimagem' in request.FILES:
            palavra.imagem = request.FILES['RCapturaimagem']
        print 'verificando video'
        if 'video' in request.FILES:
            request.FILES['video'].name = request.POST['RCapturaslug'] + ".webm"  # renomeamos o blob
            palavra.video = request.FILES['video']
            
        palavra.save();
        
        response_data = {'palavra_pk': palavra.pk}
        
    else:
        response_data = {'erro_message': 'Para salvar deve-se gravar um video e ter uma palavra digitda!'}
        
    #agora salvamos o ID ara a AP
    try:
        aprecurso = get_object_or_404(APListaRecursos, pk=request.POST['RCrecursoid'])
        dadosAP = APDados.objects.create(aprecurso=aprecurso, value=str(palavra.id), user=request.user)
        dadosAP.save()
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def grupo_palavra(request):
    print "criando grupo..."
    print request.POST['grupoNomeInput']
    
    try:
        grupo = Grupo.objects.create(nome=request.POST['grupoNomeInput'], user=request.user)
        response_data = {'aceito': 'criado', 'grupo_pk': grupo.pk, 'nome': grupo.nome}
        print grupo.nome
        print grupo.user.username
        grupo.save()
    except:
        response_data = {'aceito': 'erro'}
        
    return HttpResponse(json.dumps(response_data), content_type="application/json")