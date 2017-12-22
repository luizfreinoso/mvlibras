from django.shortcuts import HttpResponse, get_object_or_404    
import json
from texto.models import FeedBack, Texto
from AP.models import APDados, APListaRecursos
# Create your views here.
def salvarVideo(request):
    print "recebendo...." 
    response_data = {'frase_pk': 'none'}
    
    if(request.POST['RCapturaLongafrase'] != "" and 'video' in request.FILES):
        print "entrou"

        texto = Texto.objects.create(user=request.user,
                                         texto=request.POST['RCapturaLongafrase']
                                         )
        
        print 'verificando video'
        if 'video' in request.FILES:
            request.FILES['video'].name = request.POST['RCLrecursoid'] + "frase.webm"  # renomeamos o blob
            texto.video = request.FILES['video']
            
        texto.save();
        
        response_data = {'texto_pk': texto.pk}
        
    else:
        response_data = {'erro_message': 'Para salvar deve-se gravar um video e ter uma frase digitda!'}
        
    #agora salvamos o ID ara a AP
    try:
        aprecurso = get_object_or_404(APListaRecursos, pk=request.POST['RCLrecursoid'])
        dadosAP = APDados.objects.create(aprecurso=aprecurso, value=str(texto.id), user=request.user)
        dadosAP.save()
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")