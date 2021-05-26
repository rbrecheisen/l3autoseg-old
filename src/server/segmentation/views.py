from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import TensorFlowModel, DataSetModel, ImageModel, ResultModel
from rq import Queue
from redis import Redis
from .segmentation import load_model, segment_image, segment_images


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
    q = Queue(connection=Redis())
    if action == 'segment':
        images = ImageModel.objects.filter(dataset=ds).all()
        for img in images:
            job = q.enqueue(segment_image, img.file_obj.path)
            img.job_id = job.id
            img.job_status = job.get_status()
            img.save()
    images = ImageModel.objects.filter(dataset=ds).all()
    for img in images:
        if img.job_id:
            job = q.fetch_job(img.job_id)
            img.job_status = job.get_status()
            if img.job_status == 'finished':
                img.pred_file_path = job.result
            img.save()
    return render(request, 'dataset.html', context={'dataset': ds, 'images': images})

    # if action == 'segment':
    #     images = ImageModel.objects.filter(dataset=ds).all()
    #     # Build JSON that contains file paths and, eventually, prediction file
    #     # file paths for each image.
    #     img_info = {}
    #     for img in images:
    #         img_info[img.id] = {'file_path': img.file_obj.path, 'pred_file_path': ''}
    #     job = q.enqueue(segment_images, img_info)
    #     ds.job_id = job.id
    #     ds.save()
    # status = ''
    # if ds.job_id:
    #     job = q.fetch_job(ds.job_id)
    #     status = job.get_status()
    #     if status == 'finished':
    #         updated_img_info = job.result
    #         images = ImageModel.objects.filter(pk__in=updated_img_info.keys())
    #         for img in images:
    #             img.pred_file_path = updated_img_info[img.id]['pred_file_path']
    #             img.save()
    # images = ImageModel.objects.filter(dataset=ds).all()
    # return render(request, 'dataset.html', context={
    #     'dataset': ds, 'images': images, 'job_status': status})


# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/segmentation/accounts/login/')
def results(request):
    return render(request, 'results.html')


# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/segmentation/accounts/login/')
def result(request, result_id):
    return render(request, 'result.html')
