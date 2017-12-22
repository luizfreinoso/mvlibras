from django.db import models
import os
from django.contrib.auth.models import User
from django.utils import timezone
from AP.models import APListaRecursos

from  django.core.files.storage import FileSystemStorage

STATIC_CUR_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

upload_storage = FileSystemStorage(location=STATIC_CUR_DIR)

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.
# Anexos diversos
class Anexo(models.Model):
    apListaRecursos = models.ForeignKey(APListaRecursos)
    nome = models.CharField(max_length=160)
    anexo = models.FileField(upload_to='media/anexos', storage=upload_storage, default=None)
    data_criacao = models.DateTimeField('Submetido', default=timezone.now())
    pub_date = models.DateTimeField('Publicado', default=timezone.now())
    data_ultima_modificacao = models.DateTimeField('Modificado', default=timezone.now(), auto_now=True)
    publicado = models.BooleanField('Publicado?', default=True)

@receiver(pre_delete, sender=Anexo)
def anexo_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.anexo.delete(False)

@receiver(models.signals.pre_save, sender=Anexo)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `PalavraLibras` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = Anexo.objects.get(pk=instance.pk).anexo
    except Anexo.DoesNotExist:
        return False

    new_file = instance.anexo
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)