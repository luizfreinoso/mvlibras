from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Criamos a definicao da AP do professor
class AP(models.Model):
    nome = models.CharField(max_length=255)
    sigla = models.CharField(max_length=12)
    descricao = models.TextField(blank=True)
    atividades = models.TextField(blank=True)
    metodologia = models.TextField(blank=True)
    data_criacao = models.DateTimeField('Submetido', default=timezone.now())
    pub_date = models.DateTimeField('Publicado', default=timezone.now())
    data_ultima_modificacao = models.DateTimeField('Modificado', default=timezone.now())
    publicado = models.BooleanField('Publicado?', default=True)
    user = models.ForeignKey(User)

# Aqui gravamos os recuros que o professor ira utilizar
class APListaRecursos(models.Model):
    ap = models.ForeignKey(AP)
    recurso = models.IntegerField('Recurso', default=0)
    ordem = models.IntegerField('Ordem', default=0)

# Para cada recruso em uma AP, podemos ter um configuracao individual do recurso
class APConfiguracao(models.Model):
    aprecurso = models.ForeignKey(APListaRecursos)
    value = models.CharField(max_length=255)

# Cada recurso de uma AP, pode gerar um dado especifico
class APDados(models.Model):
    aprecurso = models.ForeignKey(APListaRecursos)
    value = models.TextField(blank=True)
    user = models.ForeignKey(User)
    data_criacao = models.DateTimeField('Submetido', default=timezone.now())
    pub_date = models.DateTimeField('Publicado', default=timezone.now())
    data_ultima_modificacao = models.DateTimeField('Modificado', default=timezone.now(), auto_now = True)
    publicado = models.BooleanField('Publicado?', default=True)