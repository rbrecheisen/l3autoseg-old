from django.contrib import admin
from .models import DataSetModel, ImageModel


@admin.register(DataSetModel)
class DataSetModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    pass
