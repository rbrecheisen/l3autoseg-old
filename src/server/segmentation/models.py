from django.db import models
from django.contrib.auth.models import User


class DataSetModel(models.Model):
    name = models.CharField(max_length=1024, editable=True, null=False)


class ImageModel(models.Model):
    file_obj = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    dataset = models.ForeignKey(DataSetModel, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, editable=False, related_name='+', on_delete=models.CASCADE)


class TensorFlowModel(models.Model):
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#filepathfield
    pass
