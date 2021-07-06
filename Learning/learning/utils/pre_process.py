#!/usr/bin/python3

"""
# -*- coding: utf-8 -*-

# @Time     : 2021/7/4 16:12
# @File     : pre_process.py

"""
import torch
import torchvision


class ToTensor(torchvision.transforms.ToTensor):
    def __call__(self, pic):
        default_float_dtype = torch.get_default_dtype()
        img = torchvision.transforms.PILToTensor()(pic)
        return img.to(dtype=default_float_dtype).div(255)


def normal_transform() -> torchvision.transforms.Compose:
    normal = torchvision.transforms.Compose([
        ToTensor(),  # 转化张量
    ])
    return normal


def data_augment_transform() -> torchvision.transforms.Compose:
    data_augment = torchvision.transforms.Compose([
        torchvision.transforms.RandomCrop(28),  # 随机裁剪
        torchvision.transforms.RandomHorizontalFlip(0.5),  # 水平翻转
        torchvision.transforms.RandomVerticalFlip(0.5),  # 垂直翻转
        ToTensor(),  # 转化张量
    ])
    return data_augment
