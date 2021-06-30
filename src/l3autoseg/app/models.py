import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class TensorFlowModel(models.Model):
    pass


class DataSetModel(models.Model):
    name = models.CharField(max_length=1024, editable=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    job_id = models.CharField(max_length=32, null=True)
    owner = models.ForeignKey(
        User, editable=False, related_name='+', on_delete=models.CASCADE)
    zip_file_path = models.CharField(max_length=1024, null=True)
    scores_file_path = models.CharField(max_length=1024, null=True)


@receiver(models.signals.post_delete, sender=DataSetModel)
def dataset_post_delete(sender, instance, **kwargs):
    if instance.zip_file_path and os.path.isfile(instance.zip_file_path):
        os.remove(instance.zip_file_path)
    if instance.scores_file_path and os.path.isfile(instance.scores_file_path):
        os.remove(instance.scores_file_path)


class ImageModel(models.Model):
    file_obj = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    job_status = models.CharField(max_length=16, null=True)
    pred_file_name = models.CharField(max_length=1024, null=True)
    pred_file_path = models.CharField(max_length=1024, null=True)
    png_file_name = models.CharField(max_length=1024, null=True)
    png_file_path = models.CharField(max_length=1024, null=True)
    json_file_name = models.CharField(max_length=1024, null=True)
    json_file_path = models.CharField(max_length=1024, null=True)
    dataset = models.ForeignKey(DataSetModel, on_delete=models.CASCADE)


@receiver(models.signals.post_delete, sender=ImageModel)
def image_post_delete(sender, instance, **kwargs):
    if instance.file_obj:
        if os.path.isfile(instance.file_obj.path):
            os.remove(instance.file_obj.path)
        if instance.pred_file_path and os.path.isfile(instance.pred_file_path):
            os.remove(instance.pred_file_path)
        if instance.png_file_path and os.path.isfile(instance.png_file_path):
            os.remove(instance.png_file_path)
        if instance.json_file_path and os.path.isfile(instance.json_file_path):
            os.remove(instance.json_file_path)
