import django_rq

from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files import File
from barbell2light.utils import duration
from zipfile import ZipFile
from .models import DataSetModel, ImageModel
from .segmentation import segment_images
from .rendering import create_png


# ----------------------------------------------------------------------------------------------------------------------
@login_required
def index(request):
    return render(request, 'index.html')


# ----------------------------------------------------------------------------------------------------------------------
@login_required
def datasets(request):
    if request.method == 'GET':
        objects = DataSetModel.objects.all()
        return render(request, 'datasets.html', context={'datasets': objects})
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        ds = DataSetModel.objects.create(name='dataset-{}'.format(timestamp), owner=request.user)
        for f in files:
            ImageModel.objects.create(file_obj=f, dataset=ds)
        objects = DataSetModel.objects.all()
        return render(request, 'datasets.html', context={'datasets': objects})


# ----------------------------------------------------------------------------------------------------------------------
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
        return render(request, 'datasets.html', context={'datasets': dds})
    if action == 'clear':
        ds.job_id = None
        ds.save()
        for img in images:
            img.clear_results()
        return render(request, 'dataset.html', context={'dataset': ds, 'images': images, 'time_req': time_req})
    q = django_rq.get_queue('default')
    if action == 'segment':
        job = q.enqueue(segment_images, images)
        ds.job_id = job.id
        ds.save()
        for img in images:
            img.job_status = 'queued'
            img.save()
    if ds.job_id:
        job = q.fetch_job(ds.job_id)
        if job:
            # Per-image job status may have been updated in RQ (separate thread) so we need to
            # re-retrieve the images to get these updates
            images = ImageModel.objects.filter(dataset=ds).all()
            if job.get_status() == 'finished':
                for img in images:
                    if img.png_file_name is None:
                        img.png_file_name, img.png_file_path = create_png(img)
                        img.save()
    return render(request, 'dataset.html', context={'dataset': ds, 'images': images, 'time_req': time_req})


# ----------------------------------------------------------------------------------------------------------------------
@login_required
def downloads(request, dataset_id):
    ds = DataSetModel.objects.get(pk=dataset_id)
    images = ImageModel.objects.filter(dataset=ds).all()
    zip_file_path = '/tmp/{}.zip'.format(dataset_id)
    with ZipFile(zip_file_path, 'w') as zip_obj:
        for img in images:
            zip_obj.write(img.file_obj.path)
            if img.pred_file_path:
                zip_obj.write(img.pred_file_path)
            if img.png_file_path:
                zip_obj.write(img.png_file_path)
    with open(zip_file_path, 'rb') as f:
        response = HttpResponse(File(f), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(dataset_id)
        return response
