from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/segmentation/accounts/login/')
def index(request):
    return render(request, 'segmentation.html')


@login_required(login_url='/segmentation/accounts/login/')
def datasets(request):
    return render(request, 'datasets.html')


@login_required(login_url='/segmentation/accounts/login/')
def dataset(request, dataset_id):
    return render(request, 'dataset.html')


@login_required(login_url='/segmentation/accounts/login/')
def jobs(request):
    return render(request, 'jobs.html')


@login_required(login_url='/segmentation/accounts/login/')
def job(request, job_id):
    return render(request, 'job.html')


@login_required(login_url='/segmentation/accounts/login/')
def results(request):
    return render(request, 'results.html')


@login_required(login_url='/segmentation/accounts/login/')
def result(request, result_id):
    return render(request, 'result.html')


@login_required(login_url='/segmentation/accounts/login/')
def models(request):
    return render(request, 'models.html')


@login_required(login_url='/segmentation/accounts/login/')
def model(request, model_id):
    return render(request, 'model.html')
