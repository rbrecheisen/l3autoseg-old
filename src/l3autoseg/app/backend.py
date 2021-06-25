from django.conf import settings
from .models import DataSetModel, ImageModel


def get_datasets():
    return DataSetModel.objects.all()


def get_model_dir():
    return settings.TENSORFLOW_MODEL_DIR


