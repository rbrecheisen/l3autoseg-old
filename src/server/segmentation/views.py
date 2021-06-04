import django_rq

from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from barbell2light.utils import duration, current_time_secs, elapsed_secs
from .models import DataSetModel, ImageModel
from .segmentation import segment_images
from .rendering import create_png


# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/segmentation/accounts/login/')
def index(request):
    return render(request, 'segmentation.html')


# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/segmentation/accounts/login/')
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
@login_required(login_url='/segmentation/accounts/login/')
def dataset(request, dataset_id):
    ds = DataSetModel.objects.get(pk=dataset_id)
    action = request.GET.get('action', None)
    if action == 'delete':
        ds.delete()
        dds = DataSetModel.objects.all()
        return render(request, 'datasets.html', context={'datasets': dds})
    images = ImageModel.objects.filter(dataset=ds).all()
    q = django_rq.get_queue('default')
    start_time = -1
    if action == 'segment':
        start_time = current_time_secs()
        print('starting segmentation...')
        job = q.enqueue(segment_images, images)
        ds.job_id = job.id
        ds.save()
        for img in images:
            img.job_status = 'queued'
            img.save()
    time_req = duration(8 * len(images))
    if ds.job_id:
        job = q.fetch_job(ds.job_id)
        if job and job.get_status() == 'finished':
            for img in images:
                img.job_status = 'finished'
                img.png_file_name, img.png_file_path = create_png(img)
                img.save()
            if start_time < 0:
                raise RuntimeError('Start time is -1')
            elapsed = elapsed_secs(start_time)
            print('segmentation ready after {}'.format(duration(elapsed)))
    images = ImageModel.objects.filter(dataset=ds).all()
    # for img in images:
    #     if img.job_id:
    #         job = q.fetch_job(img.job_id)
    #         if job:
    #             img.job_status = job.get_status()
    #             if img.job_status == 'finished':
    #                 img.pred_file_name, img.pred_file_path = job.result
    #                 img.png_file_name, img.png_file_path = create_png(img)
    #             img.save()
    return render(request, 'dataset.html', context={'dataset': ds, 'images': images, 'time_req': time_req})
