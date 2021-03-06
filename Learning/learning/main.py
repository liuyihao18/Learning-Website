#!/usr/bin/python3

"""
# -*- coding: utf-8 -*-

# @Time     : 2021/7/4 16:12
# @File     : main.py

"""
import argparse
import os
import sys
import time

import torch
import warnings
import datetime

from Learning.constants import time_pattern
from Learning.constants import sub_save_paths
from Learning.learning.models.lenet import LeNet
from Learning.learning.utils import data
from Learning.learning.utils import plot
from Learning.learning.utils.operate import save
from Learning.learning.utils.operate import train_evaluate

warnings.filterwarnings("ignore")  # 忽略Pytorch奇怪的警告


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=int, default=int(time.time()))
    parser.add_argument('--model', type=str, default='LeNet')
    parser.add_argument('--optimizer', type=str, default='Adam')
    parser.add_argument('--learning_rate', type=float, default=0.001)
    parser.add_argument('--batch_size', type=int, default=256)
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--num_classes', type=int, default=10)
    parser.add_argument('--use_gpu', type=bool, default=True)
    parser.add_argument('--data_path', type=str, default='data')
    parser.add_argument('--save_path', type=str, default='result')
    return parser.parse_args()


def initialize(data_path: str, save_path: str) -> None:
    try:
        os.mkdir(data_path)
    except FileExistsError:
        pass
    try:
        os.mkdir(save_path)
    except FileExistsError:
        pass
    for sub_save_path in sub_save_paths:
        try:
            os.mkdir(save_path + os.sep + sub_save_path)
        except FileExistsError:
            pass


def instance(args: dict) -> None:
    """
    :param args: 实例参数
    :return:
    """
    # 初始化
    initialize(args['data_path'], args['save_path'])
    name = str(args['id'])
    # 重定向
    log = open(args['save_path'] + os.sep + args['log'] + os.sep + name + ".log", 'w')
    stdout = sys.stdout
    sys.stdout = log

    print('--------------------------------------------------------------------')
    # 输出基本信息
    print('ID:', args['id'])
    print('Task:', args['task'])
    print('Person:', args['person'])
    print('Begin time:',
          args['begin_time'].astimezone(datetime.timezone(datetime.timedelta(hours=+8))).strftime(time_pattern))

    # 打印训练信息
    print('Use model:', args['model'])
    print('Use optimizer:', args['optimizer'])
    print('Learning rate:', args['learning_rate'])
    print('Batch size:', args['batch_size'])
    print('Epochs:', args['epochs'])

    # 确认设备
    if args['use_gpu'] and torch.cuda.is_available():
        print('Use device:', 'cuda')
        device = torch.device('cuda')
    else:
        print('Use device:', 'cpu')
        device = torch.device('cpu')

    print('--------------------------------------------------------------------')
    sys.stdout.flush()

    # 导入数据
    train_dataset, test_dataset = data.get_mnist_dateset(data_path=args['data_path'])

    # 建立模型
    if args['model'] == 'LeNet':
        model = LeNet(num_classes=args['num_classes'])
    else:
        model = LeNet(num_classes=args['num_classes'])

    # 模型训练
    loss, accuracy = train_evaluate(model=model, train_dataset=train_dataset, test_dataset=test_dataset,
                                    epochs=args['epochs'], batch_size=args['batch_size'],
                                    learning_rate=args['learning_rate'], optimizer=args['optimizer'],
                                    shuffle=True, device=device)

    # 绘制结果
    plot.plot_loss_curve(loss=loss, save_path=args['save_path'] + os.sep + args['loss_curve'], name=name)
    plot.plot_accuracy_curve(accuracy=accuracy, save_path=args['save_path'] + os.sep + args['accuracy_curve'],
                             name=name)
    # 保存模型
    save(model=model, save_path=args['save_path'] + os.sep + args['model'], name=name)

    # 关闭日志
    log.close()
    sys.stdout = stdout


if __name__ == '__main__':
    # 调用入口函数
    instance(parse_args().__dict__)
