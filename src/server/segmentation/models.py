import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class TensorFlowModel(models.Model):
    pass


class DataSetModel(models.Model):
    name = models.CharField(max_length=1024, editable=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    job_id = models.CharField(max_length=16, null=True)
    progress = models.CharField(max_length=16, null=False, default='0/0')
    owner = models.ForeignKey(
        User, editable=False, related_name='+', on_delete=models.CASCADE)


class ImageModel(models.Model):
    file_obj = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(null=False, default=False)
    pred_file_path = models.CharField(max_length=1024, null=True)
    dataset = models.ForeignKey(DataSetModel, on_delete=models.CASCADE)


@receiver(models.signals.post_delete, sender=ImageModel)
def image_post_delete(sender, instance, **kwargs):
    if instance.file_obj:
        if os.path.isfile(instance.file_obj.path):
            os.remove(instance.file_obj.path)


class ResultModel(models.Model):
    pass
