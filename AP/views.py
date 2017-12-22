from django.shortcuts import render, get_object_or_404, get_list_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from models import AP, APConfiguracao, APDados, APListaRecursos
from django.core.urlresolvers import reverse
from django.utils import timezone
from palavras.models import Palavra, Grupo
from RAnexos.models import Anexo
import json
from django import template
from asyncore import loop
from texto.models import Texto
register = template.Library()

@register.filter(name='split')
def split(value, arg):
    return value.split(arg)


# Create your views here.
@login_required
@user_passes_test(lambda u: u.groups.filter(name='professor').count() > 0, login_url='/login/')
def index(request):
    return render(request, 'painelAP.html', {'APS': AP.objects.all()})

@login_required
def ap(request, id):
    ap = get_object_or_404(AP, pk=id)
    recursos = APListaRecursos.objects.all().filter(ap=ap).order_by('ordem')
    Dgrupos = Grupo.objects.all().order_by('nome') 
    
    RAnexosDados = None
    RCDados = None
    RCLDados = None
    
    #verifica anexos
    if recursos[0].recurso == 5:
        try:
            RAnexosDados = Anexo.objects.all().filter(apListaRecursos=recursos[0])
        except:
            RAnexosDados = None
    
    #config
    try:
        if recursos[0].recurso != 5 and recursos[0].recurso != 6:
            config_aux = get_object_or_404(APConfiguracao, aprecurso=recursos[0])
            config_split = str(config_aux.value.encode('utf-8')).split('&STOP;')
            config = {}
            
            for c in config_split:
                aux = str(c).split(':')
                if aux[0] != '':
                    config[aux[0]] = aux[1]
            # print config
        else:
            config = 'None'
    except:
        config = ''
    
    #dados
    dados ={}
    try:
        dados = APDados.objects.all().filter(aprecurso=recursos[0])
    except:
        dados = {}
    
    
    #verifica videos
    if recursos[0].recurso == 2:
        try:
            RCDados = {}
            dadosID = [int(d.value) for d in dados]
            # print dadosID
            RCDados = Palavra.objects.all().filter(pk__in=dadosID)
            # print RCDados
        except:
            RCDados = None
    
    if recursos[0].recurso == 7:
        try:
            RCLDados = {}
            dadosLID = [int(d.value) for d in dados]
            # print dadosLID
            RCLDados = Texto.objects.all().filter(pk__in=dadosLID)
            # print RCLDados
        except:
            RCLDados = None
    
    return render(request, 'AP.html', {'ap': ap, 'recurso': recursos[0], 'Dgrupos' : Dgrupos,
                                       'RAnexosDados': RAnexosDados, 'numRecursos': int(recursos.count()-1),
                                       'indexR': 0, 'config': config,
                                       'RCDados': RCDados, 'RCLDados': RCLDados, 'dadosAP': dados
                                       })
    
@login_required
def apordem(request, id, ordem):
    ap = get_object_or_404(AP, pk=id)
    recursos = APListaRecursos.objects.all().filter(ap=ap).order_by('ordem')
    Dgrupos = Grupo.objects.all().order_by('nome')
    
    RAnexosDados = None
    RCDados = None
    RCLDados = None
    
    #verifica anexos
    if recursos[int(ordem)].recurso == 5:
        try:
            RAnexosDados = Anexo.objects.all().filter(apListaRecursos=recursos[int(ordem)])
        except:
            RAnexosDados = None
    
    #config
    try:
        if recursos[int(ordem)].recurso != 5 and recursos[int(ordem)].recurso != 6:
            config_aux = get_object_or_404(APConfiguracao, aprecurso=recursos[int(ordem)])
            config_split = str(config_aux.value.encode('utf-8')).split('&STOP;')
            config = {}
            
            for c in config_split:
                aux = str(c).split(':')
                if aux[0] != '':
                    config[aux[0]] = aux[1]
            # print config
        else:
            config = 'none'
    except:
        config = ''
        
    #dados
    dados ={}
    try:
        dados = APDados.objects.all().filter(aprecurso=recursos[int(ordem)])
    except:
        dados = {}
    
    
    #verifica videos
    if recursos[int(ordem)].recurso == 2:
        try:
            RCDados = {}
            dadosID = [int(d.value) for d in dados]
            # print dadosID
            RCDados = Palavra.objects.all().filter(pk__in=dadosID)
            # print RCDados
        except:
            RCDados = None
            
    if recursos[int(ordem)].recurso == 7:
        try:
            RCLDados = {}
            dadosLID = [int(d.value) for d in dados]
            # print dadosLID
            RCLDados = Texto.objects.all().filter(pk__in=dadosLID)
            # print RCLDados
        except:
            RCLDados = None
    
    return render(request, 'AP.html', {'ap': ap, 'recurso': recursos[int(ordem)], 'Dgrupos' : Dgrupos,
                                       'RAnexosDados': RAnexosDados, 'numRecursos': int(recursos.count()-1),
                                       'indexR': int(ordem), 'config': config,
                                       'dadosAP' : dados, 'RCLDados': RCLDados, 'RCDados':RCDados
                                       })

@login_required
@user_passes_test(lambda u: u.groups.filter(name='professor').count() > 0, login_url='/login/')
def criar(request):
    return render(request, 'criarAP.html')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='professor').count() > 0, login_url='/login/')
def criarNovaAP(request):
    nome = request.POST['nome']
    sigla = request.POST['sigla']
    desc = request.POST['descricao']
    atividades = request.POST['atividades']
    metodologia = request.POST['metodologia']
    
    recursos = request.POST.getlist('recursos')
    
    # print recursos
    if len(request.POST.getlist('publicado')) > 0:
        publicado = True
    else:
        publicado = False
    
    # print publicado
    
    if len(recursos) > 0:
        ap = AP.objects.create(nome=nome, sigla=sigla, descricao=desc, 
                               atividades=atividades, metodologia=metodologia, publicado=publicado,
                               user=request.user)
        for i, item in enumerate(recursos):
            aprecurso = APListaRecursos.objects.create(ap=ap, recurso=int(item), ordem=i)
        ap.save()
        return HttpResponseRedirect(reverse('aps:configurarAP', args=(ap.id,)));
    else:
        return render(request, 'criarAP.html', {'error_message': 'Selecione um recurso digital!'})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='professor').count() > 0, login_url='/login/')
def duplicar(request, id):
    ap = get_object_or_404(AP, pk=id)
    ap.user = request.user
    recursos = get_list_or_404(APListaRecursos, ap=ap)
    
    ap.pk = None
    ap.save()
    
    for recurso in recursos:
        recurso.pk = None
        recurso.ap = ap
        recurso.save()
    
    return HttpResponseRedirect('/aps/')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='professor').count() > 0, login_url='/login/')
def removerAP(request, id):
    ap = get_object_or_404(AP, pk=id)
    ap.delete()
    return render(request, 'painelAP.html', {'sucess_message': "AP excluida com sucesso!",
                                           'APS': AP.objects.all()})
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='professor').count() > 0, login_url='/login/')
def editarAP(request, id):
    ap = get_object_or_404(AP, pk=id)
    return render(request, 'editarAP.html', {'ap': ap,})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='professor').count() > 0, login_url='/login/')
def SalvarAtualizacaoAP(request, id):
    ap = get_object_or_404(AP, pk=id)
    nome = request.POST['nome']
    sigla = request.POST['sigla']
    desc = request.POST['descricao']
    atividades = request.POST['atividades']
    metodologia = request.POST['metodologia']
    
    if len(request.POST.getlist('publicado')) > 0:
        ap.publicado = True
        ap.pub_date = timezone.now()
    else:
        ap.publicado = False

    ap.nome = nome
    ap.sigla = sigla
    ap.descricao = desc
    ap.atividades = atividades
    ap.metodologia = metodologia
    ap.data_ultima_modificacao = timezone.now()
    
    ap.save()

    return render(request, 'painelAP.html', {'sucess_message': 
                                                'AP ' + nome + '[' + sigla +']' + ' atualizada com sucesso!',
                                            'APS': AP.objects.all()})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='professor').count() > 0, login_url='/login/')
def configurarAP(request, id):
    ap = get_object_or_404(AP, pk=id)
    recursos = APListaRecursos.objects.all().filter(ap=ap).order_by('ordem')
    Dgrupos = Grupo.objects.all().order_by('nome') 
    
    RAnexosDados = None
    RHTMLDados = None
    
    #verifica anexos
    for recurso in recursos:
        # print recurso.recurso
        if recurso.recurso == 5:
            try:
                RAnexosDados = Anexo.objects.all().filter(apListaRecursos=recurso)
            except:
                RAnexosDados = None
        
        if recurso.recurso == 6:
            try:
                RHTMLDados = APDados.objects.all().filter(aprecurso=recurso)
            except:
                RHTMLDados = None
    
    # print RAnexosDados 
    # print RHTMLDados 
    #config
    configs = {}
    try:
        for recurso in recursos:
            if recurso.recurso != 5 and recurso.recurso != 6:
                config_aux = get_object_or_404(APConfiguracao, aprecurso=recurso)
                config_split = str(config_aux.value.encode('utf-8')).split('&STOP;')
                config = {}
                
                for c in config_split:
                    aux = str(c).split(':')
                    if aux[0] != '':
                        config[aux[0]] = aux[1]
                #Lista de configs para os recursos
                configs[recurso.recurso] = config
                # print configs
            else:
                configs[recurso.recurso] = {}
    except:
        configs = {}
    
    # print configs
    
    return render(request, 'configurarAP.html', {'ap': ap, 'recursos': recursos, 'Dgrupos' : Dgrupos,
                                                 'RAnexosDados': RAnexosDados, 'configs':configs,
                                                 'RHTMLDados': RHTMLDados})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='professor').count() > 0, login_url='/login/')
def salvarConfiguracaoAP(request, id, ordem):
    recurso = get_object_or_404(APListaRecursos, pk=int(id))
    #Ateramos a ordem desenjada
    recurso.ordem = ordem
    recurso.save()
    
    valores = ''
    response_data = {}
    
    for key, value in request.POST.iteritems():
        if key != "csrfmiddlewaretoken":
            # se for HTML
            if key == "RHTMLTexto":
                try:
                    textohtml = get_object_or_404(APDados, aprecurso=recurso)
                    textohtml.value = value
                    textohtml.user = request.user
                    textohtml.save()
                except:
                    textohtml = APDados.objects.create(aprecurso=recurso, value=value, user=request.user)
                    textohtml.save()
            else:
                valores += key + ':' + value + '&STOP;'
        
    # verificamos se ja tem configuracoes
    try:
        config = APConfiguracao.objects.get(aprecurso=recurso)
        config.value = valores
        config.save()
    except APConfiguracao.DoesNotExist:
        if valores != '':
            config = APConfiguracao.objects.create(aprecurso=recurso, value=valores)
            config.save()
            
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def salvarLog(request, id):
    recurso = get_object_or_404(APListaRecursos, pk=int(id))
    response_data = {}
    # print 'salvanso LOG..' + id
    #print request.POST['log']
    # verificamos se ja tem dados para este usuario
    try:
        logD = APDados.objects.get(aprecurso=recurso, user=request.user)
        logD.value = request.POST['log']
        logD.save()
    except APDados.DoesNotExist:
        # print 'Novo Log'
        if request.POST['log'] != '':
            logD = APDados.objects.create(aprecurso=recurso, value=request.POST['log'], user=request.user)
            logD.save()
    
    # print 'salvo'
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")