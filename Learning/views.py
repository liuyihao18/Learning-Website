import datetime
import math
import platform
import time

import torch

from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone

from . import models
from . import constants


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


def result_index(request, page=1):
    objs = models.ModelInfo.objects.all().order_by('-id')  # 增加'-'表示逆序
    max_page = math.ceil(objs.count() / constants.page_size)  # 最大页数
    if page < 1:
        return redirect('/result/1/')  # 重定向
    if page > max_page:
        return redirect('/result/' + str(max_page) + '/')  # 重定向
    left = (page - 1) * constants.page_size  # 左索引
    right = min(page * constants.page_size, objs.count())  # 右索引
    objs = objs[left:right]  # 取出部分数据
    context = {
        'active': 'result',
        'cols': constants.cols,
        'col_names': constants.col_names,
        'objs': objs,
    }
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
    return redirect('/result/')
