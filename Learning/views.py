import platform
import torch

from django.shortcuts import redirect
from django.shortcuts import render

from . import models
from . import logic


# Create your views here.
def learning_index(request):
    context = {
        'active': 'index',
        'python_version': platform.python_version(),
        'pytorch_version': torch.__version__
    }
    return render(request, 'Learning/index.html', context)


def train_index(request):
    context = {
        'active': 'train'
    }
    return render(request, 'Learning/train.html', context)


def result_index(request, page=1, item=1, want='table'):
    if want == 'table':
        context = logic.get_table_context(page)
    elif want == 'log':
        context = logic.get_log_context(page, item)
    elif want == 'result':
        context = logic.get_result_context(page, item)
    else:
        context = {'redirect': '/result/' + str(page) + '/'}

    if 'redirect' in context:
        return redirect(context['redirect'])

    context['want'] = want
    return render(request, 'Learning/result.html', context)


def post(request):
    args = {
        'model': request.POST['model'],
        'optimizer': request.POST['optimizer'],
        'learning_rate': request.POST['learning_rate'],
        'batch_size': request.POST['batch_size'],
        'epochs': request.POST['epochs'],
        'task': request.POST['task'],
        'person': request.POST['person'],
        'state': 'train',
    }
    models.ModelInfo.objects.create(**args)
    return redirect('/result/1/')
