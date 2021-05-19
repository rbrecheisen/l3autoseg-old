import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class TensorFlowModel(models.Model):
    pass


class DataSetModel(models.Model):
    name = models.CharField(max_length=1024, editable=True, null=False)


class ImageModel(models.Model):
    file_obj = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    dataset = models.ForeignKey(DataSetModel, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, editable=False, related_name='+', on_delete=models.CASCADE)


@receiver(models.signals.post_delete, sender=ImageModel)
def image_post_delete(sender, instance, **kwargs):
    if instance.file_obj:
        if os.path.isfile(instance.file_obj.path):
            os.remove(instance.file_obj.path)


class ResultModel(models.Model):
    pass
