from django.shortcuts import render, HttpResponse, get_object_or_404
from RAnexos.models import Anexo
from AP.models import APListaRecursos
import json

# Create your views here.
def anexar(request):
    print 'anexando....'
    response_data = {}
    print request.POST['RAnexosRecursoID']
    print request.POST['RAnexosNomeArquivo']
    print request.FILES['RAnexosArquivoNovo'].name
    
    apListaRecurso = get_object_or_404(APListaRecursos, pk=request.POST['RAnexosRecursoID'])
    
    if 'RAnexosArquivoNovo' in request.FILES:
        print 'criando dado..'
        anexo = Anexo.objects.create(apListaRecursos = apListaRecurso,nome = request.POST['RAnexosNomeArquivo'],anexo = request.FILES['RAnexosArquivoNovo'])
        anexo.save()
        print 'salvando..'
        response_data = {'message': 'Arquivo enviado!', 
                         'iditem': str(anexo.id), 
                         'nomeitem': anexo.nome, 
                         'linkitem': str(anexo.anexo)
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data = {'message': 'Arquivo falhou! Verifique novamente!'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
def habilitar_desabilitar(reuqest,id):
    anexo = get_object_or_404(Anexo, pk=id)
    response_data = {}
    
    if(anexo.publicado):
        anexo.publicado = False
    else:
        anexo.publicado = True
    
    anexo.save()
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def excluir(request,id):
    anexo = get_object_or_404(Anexo, pk=id)
    print anexo.nome
    response_data = {}
    
    anexo.delete()
    
    response_data = {'message': 'Deletado com sucesso!'}
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")