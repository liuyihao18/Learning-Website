import platform
import time

import torch

from django.shortcuts import redirect
from django.shortcuts import render

from Learning import constants
from Learning import logic
from Learning import models
from Learning.task import Task


# Create your views here.
# 主页
def learning_index(request):
    context = {
        'active': 'index',  # 当前active
        'python_version': platform.python_version(),  # python版本
        'pytorch_version': torch.__version__  # pytorch版本
    }
    return render(request, 'Learning/index.html', context)


# 训练页面
def train_index(request):
    context = {
        'active': 'train',  # 当前active
        'model_options': constants.model_options,  # 模型选项
        'optimizer_options': constants.optimizer_options,  # 优化器选项
    }
    return render(request, 'Learning/train.html', context)


# 任务列表页面
def task_list_index(request, page=None, anything=None):
    # 如果是一些可以理解的url，则重定向
    if page is None:
        return redirect('/result/1/')
    if anything is not None:
        return redirect('/result/' + str(page) + '/')
    # 获取context
    context = logic.get_task_list_context(page)
    # 当前active
    context['active'] = 'result'
    # 如果是重定向则重定向
    if 'redirect' in context:
        return redirect(context['redirect'])
    else:
        return render(request, 'Learning/result/task_list.html', context)


# 日志页面
def log_index(request, page, item):
    # 获取context
    context = logic.get_log_context(page, item)
    # 当前active
    context['active'] = 'result'
    return render(request, 'Learning/result/log.html', context)


# 分析页面
def analysis_index(request, page, item):
    # 获取context
    context = logic.get_analysis_context(page, item)
    # 当前active
    context['active'] = 'result'
    return render(request, 'Learning/result/analysis.html', context)


# 删除
def delete(request, page, item):
    # 获取context
    context = logic.get_delete_context(page, item)
    # 重定向
    return redirect(context['redirect'])


# 清理
def clean(request):
    # 获取context
    context = logic.get_clean_context()
    # 重定向
    return redirect(context['redirect'])


# 上传
def post(request):
    # 获取参数
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
    # 创建对象
    models.ModelInfo.objects.create(**args)
    # 派发任务
    task = Task(models.ModelInfo.objects.last().id)
    task.start()
    # 重定向
    return redirect('/result/1/')
