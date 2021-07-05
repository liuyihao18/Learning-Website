import datetime
import platform
import time

import torch

from django.shortcuts import redirect
from django.shortcuts import render
from . import models


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


def result_index(request, page_num=1):
    objs = models.ModelInfo.objects.all().order_by('-id')  # 增加'-'表示逆序
    # (objs[0].begin_time - objs[1].begin_time).total_seconds()  # Time操作
    print(objs.count())
    print()
    for obj in objs:
        obj.finish_time = datetime.datetime.now()
        print(obj.begin_time)
        print(obj.finish_time)
        obj.save()

    # TODO: 把数据表用table分页显示出来
    context = {
        'active': 'result'
    }
    return render(request, 'Learning/result.html', context)


def post(request):
    args = {
        'id': int(time.time()),
        'model': request.POST['model'],
        'optimizer': request.POST['optimizer'],
        'learning_rate': request.POST['learning_rate'],
        'batch_size': request.POST['batch_size'],
        'epochs': request.POST['epochs'],
        'task': request.POST['task'],
        'person': request.POST['person'],
        'state': 'train',
        'num_classes': 10,
        'use_gpu': True,
        'data_path': 'data',
        'save_path': 'result',
    }
    models.ModelInfo.objects.create(
        id=int(time.time()),
        model=request.POST['model'],
        optimizer=request.POST['optimizer'],
        learning_rate=request.POST['learning_rate'],
        batch_size=request.POST['batch_size'],
        epochs=request.POST['epochs'],
        task=request.POST['task'],
        person=request.POST['person'],
        state='train',
    )
    return redirect('/result/')
