from django.shortcuts import HttpResponse, get_object_or_404    
import json
from texto.models import Texto
from AP.models import APDados, APListaRecursos
# Create your views here.
def salvarVideo(request):
    print "recebendo...." 
    response_data = {'frase_pk': '0'}
    
    if(request.POST['RDVResposta'] != "" and 'video' in request.FILES):
        print "entrou"

        texto = Texto.objects.create(user=request.user,
                                         texto=request.POST['RDVResposta']
                                         )
        
        print 'verificando video'
        if 'video' in request.FILES:
            request.FILES['video'].name = request.POST['RDVrecursoid'] + "frase.webm"  # renomeamos o blob
            texto.video = request.FILES['video']
            
        texto.save();
        
        response_data = {'texto_pk': texto.pk, 'video_link': texto.video.url}
        
    else:
        response_data = {'erro_message': 'Para salvar deve-se gravar um video e ter uma frase digitda!'}
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")