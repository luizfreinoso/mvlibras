import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from  django.core.files.storage import FileSystemStorage

STATIC_CUR_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

upload_storage = FileSystemStorage(location=STATIC_CUR_DIR)

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.
# Nosso texto tem um conjunto de palavras chaves, que sao os grupos
class Texto(models.Model):
    user = models.ForeignKey(User)
    texto = models.TextField('Texto', blank=True)
    video = models.FileField(upload_to='media/videosfrasesenviados', storage=upload_storage, default="media/none.mp4")
    data_criacao = models.DateTimeField('Submetido', default=timezone.now())
    pub_date = models.DateTimeField('Publicado', default=timezone.now())
    data_ultima_modificacao = models.DateTimeField('Modificado', default=timezone.now())
    publicado = models.BooleanField('Publicado?', default=True)
    
    def __unicode__(self):
        return self.texto
    
class FeedBack(models.Model):
    texto = models.ForeignKey(Texto)
    user = models.ForeignKey(User)
    comentario = models.TextField()
    data_criacao = models.DateTimeField('Submetido', default=timezone.now())
    pub_date = models.DateTimeField('Publicado', default=timezone.now())
    data_ultima_modificacao = models.DateTimeField('Modificado', default=timezone.now())
    publicado = models.BooleanField('Publicado?', default=True)
    
@receiver(pre_delete, sender=Texto)
def palavra_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.video.delete(False)

@receiver(models.signals.pre_save, sender=Texto)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `PalavraLibras` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = Texto.objects.get(pk=instance.pk).video
    except Texto.DoesNotExist:
        return False

    new_file = instance.video
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)