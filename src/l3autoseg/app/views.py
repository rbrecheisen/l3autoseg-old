import json
import django_rq
import pandas as pd

from os.path import basename
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files import File
from barbell2light.utils import duration
from zipfile import ZipFile
from .models import DataSetModel, ImageModel
from .scoring import score_images


@login_required
def datasets(request):
    if request.method == 'GET':
        objects = DataSetModel.objects.all()
        return render(request, 'datasets.html', context={
            'datasets': objects, 'model_dir': settings.TENSORFLOW_MODEL_DIR})
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        ds = DataSetModel.objects.create(name='dataset-{}'.format(timestamp), owner=request.user)
        for f in files:
            ImageModel.objects.create(file_obj=f, dataset=ds)
        objects = DataSetModel.objects.all()
        return render(request, 'datasets.html', context={
            'datasets': objects, 'model_dir': settings.TENSORFLOW_MODEL_DIR})


@login_required
def dataset(request, dataset_id):
    ds = DataSetModel.objects.get(pk=dataset_id)
    images = ImageModel.objects.filter(dataset=ds).all()
    # Time required: 11s for GPU initialization, 0.5s per image
    time_req = duration(int(11 + 0.5 * len(images)) + 1)
    action = request.GET.get('action', None)
    if action == 'delete':
        ds.delete()
        dds = DataSetModel.objects.all()
        return render(request, 'datasets.html', context={
            'datasets': dds, 'model_dir': settings.TENSORFLOW_MODEL_DIR})
    q = django_rq.get_queue('default')
    if action == 'score':
        job = q.enqueue(score_images, images)
        ds.job_id = job.id
        ds.save()
        for img in images:
            img.job_status = 'queued'
            img.save()
    # if ds.job_id:
    #     # TODO: Move this code to scoring.py because refreshing the page causes the PNGs
    #     # to be created. This is very time-consuming and blocks the page.
    #     job = q.fetch_job(ds.job_id)
    #     if job:
    #         # Per-image job status may have been updated in RQ (separate thread) so we need to
    #         # re-retrieve the images to get these updates
    #         images = ImageModel.objects.filter(dataset=ds).all()
    #         if job.get_status() == 'finished':
    #             for img in images:
    #                 if img.png_file_name is None:
    #                     img.png_file_name, img.png_file_path = create_png(img)
    #                     img.save()
    return render(request, 'dataset.html', context={
        'dataset': ds, 'images': images, 'time_req': time_req, 'model_dir': settings.TENSORFLOW_MODEL_DIR})


def add_to_zip(file_path, zip_obj):
    zip_obj.write(file_path, arcname=basename(file_path))


def collect_scores(images):
    scores = {'file_name': [], 'smra': [], 'muscle_area': [], 'vat_area': [], 'sat_area': []}
    for img in images:
        with open(img.json_file_path, 'r') as f:
            data = json.load(f)
        scores['file_name'].append(img.file_obj.name)
        scores['smra'].append(data['smra'])
        scores['muscle_area'].append(data['muscle_area'])
        scores['vat_area'].append(data['vat_area'])
        scores['sat_area'].append(data['sat_area'])
    return pd.DataFrame(data=scores)


@login_required
def downloads(request, dataset_id):
    ds = DataSetModel.objects.get(pk=dataset_id)
    images = ImageModel.objects.filter(dataset=ds).all()
    zip_file_path = '/tmp/{}.zip'.format(ds.name)
    with ZipFile(zip_file_path, 'w') as zip_obj:
        for img in images:
            add_to_zip(img.file_obj.path, zip_obj)
            if img.pred_file_path:
                add_to_zip(img.pred_file_path, zip_obj)
            if img.png_file_path:
                add_to_zip(img.png_file_path, zip_obj)
            if img.json_file_path:
                add_to_zip(img.json_file_path, zip_obj)
        scores = collect_scores(images)
        scores_file_path = '/tmp/{}-scores.csv'.format(ds.name)
        scores.to_csv(scores_file_path, index=False)
        add_to_zip(scores_file_path, zip_obj)
    ds.zip_file_path = zip_file_path
    ds.scores_file_path = scores_file_path
    ds.save()
    with open(zip_file_path, 'rb') as f:
        response = HttpResponse(File(f), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(ds.name)
        return response
