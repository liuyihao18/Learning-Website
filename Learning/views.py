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


def task_list_index(request, page=None, anything=None):
    if page is None:
        return redirect('/result/1/')
    if anything is not None:
        return redirect('/result/' + str(page) + '/')
    context = logic.get_task_list_context(page)
    context['active'] = 'result'
    return render(request, 'Learning/result/task_list.html', context)


def log_index(request, page, item):
    context = logic.get_log_context(page, item)
    context['active'] = 'result'
    return render(request, 'Learning/result/log.html', context)


def analysis_index(request, page, item):
    context = logic.get_analysis_context(page, item)
    context['active'] = 'result'
    return render(request, 'Learning/result/analysis.html', context)


def delete(request, page, item):
    context = logic.get_delete_context(page, item)
    return redirect(context['redirect'])


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
