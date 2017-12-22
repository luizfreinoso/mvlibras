from django.db import models
import os
from django.contrib.auth.models import User
from django.utils import timezone

from  django.core.files.storage import FileSystemStorage

STATIC_CUR_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

upload_storage = FileSystemStorage(location=STATIC_CUR_DIR)

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.
# Grupo que a palavra pertence, ex: fruta, legumes, etc...
class Grupo(models.Model):
    nome = models.CharField(max_length=45)
    user = models.ForeignKey(User)
    data_criacao = models.DateTimeField('Submetido', default=timezone.now())
    pub_date = models.DateTimeField('Publicado', default=timezone.now())
    data_ultima_modificacao = models.DateTimeField('Modificado', default=timezone.now())
    publicado = models.BooleanField('Publicado?', default=True)
    
    def __unicode__(self):
        return self.nome
    
# Palavra com video e imagem
class Palavra(models.Model):
    nome = models.CharField(max_length=45) #Palavra Digitada
    dicionario = models.IntegerField('Dicionario', default=2) # 1-ines,2-pessoal,3-grupo
    video = models.FileField(upload_to='media/videosenviados', storage=upload_storage, default="media/none.mp4")
    imagem = models.FileField(upload_to='media/videosenviados/referencia', storage=upload_storage, default="media/none.png")
    grupo = models.ForeignKey(Grupo)
    slug = models.CharField(max_length=45) # nome unico, identificador
    user = models.ForeignKey(User)
    pontuacao_media = models.DecimalField('Media',max_digits=5, decimal_places=2, default=0)
    peso = models.DecimalField('peso',max_digits=5, decimal_places=2, default=0)
    data_criacao = models.DateTimeField('Submetido', default=timezone.now())
    pub_date = models.DateTimeField('Publicado', default=timezone.now())
    data_ultima_modificacao = models.DateTimeField('Modificado', default=timezone.now())
    publicado = models.BooleanField('Publicado?', default=False)
    
    def __unicode__(self):
        return self.nome

# Avaliacao individual para uma palavra, votos de cada avaliador para uma palavra
# precisamos do palavra-has_usuario pois avaliamos uma palavra de um usuario
# especifico
class palavra_avaliacao(models.Model):
    user = models.ForeignKey(User)
    palavra = models.ForeignKey(Palavra)
    nota = models.IntegerField('Nota', default=0)
    pub_date = models.DateTimeField('Publicado', default=timezone.now())

@receiver(pre_delete, sender=Palavra)
def palavra_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.imagem.delete(False)
    instance.video.delete(False)

@receiver(models.signals.pre_save, sender=Palavra)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `PalavraLibras` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = Palavra.objects.get(pk=instance.pk).imagem
        old_file2 = Palavra.objects.get(pk=instance.pk).video
    except Palavra.DoesNotExist:
        return False

    new_file = instance.imagem
    new_file2 = instance.video
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
    if not old_file2 == new_file2:
        if os.path.isfile(old_file2.path):
            os.remove(old_file2.path)
