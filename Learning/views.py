import platform
import time

import torch

from django.shortcuts import redirect
from django.shortcuts import render

from Learning import interface
from Learning import logic
from Learning import models


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
        context = logic.get_task_list_context(page)
    elif want == 'log':
        context = logic.get_log_context(page, item)
    elif want == 'result':
        context = logic.get_result_context(page, item)
    elif want == 'delete':
        context = logic.get_delete_context(page, item)
    else:
        context = {'redirect': '/result/' + str(page) + '/'}

    if 'redirect' in context:
        return redirect(context['redirect'])

    context['want'] = want
    return render(request, 'Learning/result.html', context)


def task_list_index(request, page=None, anything=None):
    if page is None:
        return redirect('/result/1/')
    if anything is not None:
        return redirect('/result/' + str(page) + '/')
    context = logic.get_task_list_context(page)
    return render(request, 'Learning/result/task_list.html', context)


def log_index(request, page, item):
    context = logic.get_log_context(page, item)
    return render(request, 'Learning/result/log.html', context)
    pass


def analysis_index(request, item):
    pass


def delete(request, item):
    pass


def post(request):
    args = {
        'id': int(time.time() * 1000),
        'model': request.POST['model'],
        'optimizer': request.POST['optimizer'],
        'learning_rate': request.POST['learning_rate'],
        'batch_size': request.POST['batch_size'],
        'epochs': request.POST['epochs'],
        'task': request.POST['task'],
        'person': request.POST['person'],
        'state': 'wait',
    }
    models.ModelInfo.objects.create(**args)
    task = interface.Task(models.ModelInfo.objects.last().id)
    task.start()
    return redirect('/result/1/')
