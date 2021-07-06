#!/usr/bin/python3

"""
# -*- coding: utf-8 -*-

# @Time     : 2021/7/4 20:31
# @File     : plot.py

"""
import os

import matplotlib.pyplot as plt
import numpy as np
import time


def plot_data_curve(data: list[any], save_path: str, name: str, **kwargs) -> None:
    """
    :param data: 二维列表，(i, j)代表每一个数值是第i个epoch中第j个batch的loss
    :param save_path: 保存图片的文件夹路径
    :param name:  保存图片的名称
    :return: figure
    """
    # 绘制图像
    plt.figure()
    plt.plot(data, '-*', label=kwargs['label'], color=kwargs['color'])
    plt.legend()
    plt.xlabel(kwargs['xlabel'])
    plt.ylabel(kwargs['ylabel'])
    plt.title(kwargs['title'])

    # 保存图像并显示
    if save_path.endswith(os.sep):
        filename = save_path + name
    else:
        filename = save_path + os.sep + name
    plt.savefig(fname=filename)
    # plt.show()


def plot_loss_curve(loss: list[list[float]], save_path: str, name: str = str(int(time.time()))) -> None:
    """
    :param loss: 一维列表，(i)代表第i个epoch中的accuracy
    :param save_path: 保存图片的文件夹路径
    :param name:  保存图片的名称
    :return: figure
    """
    # 把loss对每个epoch取平均
    loss = list(map(lambda loss_epoch: np.mean(loss_epoch), loss))
    # 绘制图像
    plot_data_curve(loss, save_path, name, label='loss', color='blue', xlabel='epoch', ylabel='loss',
                    title='Loss Curve')


def plot_accuracy_curve(accuracy: list[float], save_path: str, name: str = str(int(time.time()))) -> None:
    """
    :param accuracy: 一维列表，(i)代表第i个epoch中的accuracy
    :param save_path: 保存图片的文件夹路径
    :param name:  保存图片的名称
    :return: figure
    """
    # 绘制图像
    plot_data_curve(accuracy, save_path, name, label='accuracy', color='coral', xlabel='epoch', ylabel='accuracy',
                    title='Accuracy Curve')
