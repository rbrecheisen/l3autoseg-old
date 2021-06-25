from django.conf import settings
from barbell2light.dicom import is_dicom_file
from .models import DataSetModel, ImageModel


def get_datasets():
    return DataSetModel.objects.all()


def create_dataset(files):
    errors = []
    for f in files:
        if not is_dicom_file(f):
            err = 'File {} is not a DICOM file'.format(f)
            errors.append(err)
            print(err)
        else:
            print('File is DICOM')
    return 0


def get_model_dir():
    return settings.TENSORFLOW_MODEL_DIR


