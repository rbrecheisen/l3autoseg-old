from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import DataSetModel, ImageModel
from rq import Queue
from redis import Redis
from .segmentation import segment_image
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
        datasets = DataSetModel.objects.all()
        return render(request, 'datasets.html', context={'datasets': datasets})
    q = Queue(connection=Redis())
    if action == 'segment':
        images = ImageModel.objects.filter(dataset=ds).all()
        # We're creating a new job for every image so that we can track the status per image
        for img in images:
            job = q.enqueue(segment_image, img.file_obj.path)
            img.job_id = job.id
            img.job_status = job.get_status()
            img.save()
    images = ImageModel.objects.filter(dataset=ds).all()
    nr_secs = 8 * len(images)
    for img in images:
        if img.job_id:
            job = q.fetch_job(img.job_id)
            if job:
                img.job_status = job.get_status()
                if img.job_status == 'finished':
                    img.pred_file_name, img.pred_file_path = job.result
                    img.png_file_name, img.png_file_path = create_png(img)
                img.save()
    return render(request, 'dataset.html', context={'dataset': ds, 'images': images, 'nr_secs': nr_secs})
