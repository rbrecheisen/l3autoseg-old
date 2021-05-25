from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import TensorFlowModel, DataSetModel, ImageModel, ResultModel
from rq import Queue
from redis import Redis
from .segmentation import segment_files


# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/segmentation/accounts/login/')
def index(request):
    return render(request, 'segmentation.html')


# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/segmentation/accounts/login/')
def models(request):
    return render(request, 'models.html')


# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/segmentation/accounts/login/')
def model(request, model_id):
    return render(request, 'model.html')


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
        objects = DataSetModel.objects.all()
        return render(request, 'datasets.html', context={'datasets': objects})
    files = ImageModel.objects.filter(dataset=ds).all()
    q = Queue(connection=Redis())
    if action == 'segment':
        job = q.enqueue(segment_files, files)
        ds.job_id = job.id
        ds.save()
    job = q.fetch_job(ds.job_id)
    return render(request, 'dataset.html', context={
        'dataset': ds, 'files': files, 'job_status': job.get_status()})


# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/segmentation/accounts/login/')
def results(request):
    return render(request, 'results.html')


# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/segmentation/accounts/login/')
def result(request, result_id):
    return render(request, 'result.html')
