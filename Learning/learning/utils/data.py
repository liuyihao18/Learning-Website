#!/usr/bin/python3

"""
# -*- coding: utf-8 -*-

# @Time     : 2021/7/4 16:12
# @File     : data.py

"""
import torchvision

from torch.utils.data import Dataset
from Learning.learning.utils import pre_process


def get_mnist_dateset(data_path: str) -> (Dataset, Dataset):
    # MNIST dataset
    train_dataset = torchvision.datasets.MNIST(root=data_path,
                                               train=True,
                                               transform=pre_process.data_augment_transform(),
                                               download=True)

    test_dataset = torchvision.datasets.MNIST(root=data_path,
                                              train=False,
                                              transform=pre_process.normal_transform())

    return train_dataset, test_dataset
