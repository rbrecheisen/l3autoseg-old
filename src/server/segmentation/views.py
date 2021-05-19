from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/segmentation/accounts/login/')
def index(request):
    return render(request, 'segmentation.html')


@login_required(login_url='/segmentation/accounts/login/')
def models(request):
    pass


@login_required(login_url='/segmentation/accounts/login/')
def model(request, model_id):
    pass


@login_required(login_url='/segmentation/accounts/login/')
def datasets(request):
    pass


@login_required(login_url='/segmentation/accounts/login/')
def dataset(request, dataset_id):
    pass


@login_required(login_url='/segmentation/accounts/login/')
def jobs(request):
    pass


@login_required(login_url='/segmentation/accounts/login/')
def job(request, job_id):
    pass


@login_required(login_url='/segmentation/accounts/login/')
def results(request):
    pass


@login_required(login_url='/segmentation/accounts/login/')
def result(request, result_id):
    pass
