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


def post(request):
    print(request.POST)
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
