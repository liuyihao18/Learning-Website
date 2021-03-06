#!/usr/bin/python3

"""
# -*- coding: utf-8 -*-

# @Time     : 2021/7/4 16:12
# @File     : operate.py

"""
import os
import sys

import torch

from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from typing import List


def train():
    pass


def evaluate(model: torch.nn.Module, test_loader: DataLoader, device: torch.device) -> float:
    model.eval()  # 验证模式
    correct = 0  # 正确
    total = 0  # 总数
    with torch.no_grad():
        for data, labels in test_loader:
            data, labels = data.to(device), labels.to(device)
            outputs = model(data)
            _, predicted = torch.max(outputs.data, 1)
            correct += (predicted == labels).sum().item()
            total += len(labels)

    print('Test Accuracy of the model is: {} %'.format(100 * correct / total))
    return correct / total


def train_evaluate(model: torch.nn.Module, train_dataset: Dataset, test_dataset: Dataset,
                   epochs: int, batch_size: int, learning_rate: float, optimizer: str,
                   shuffle: bool = True, device: torch.device = torch.device('cpu'), evaluate_mode: bool = True
                   ) -> (List[List[float]], List[float]):
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle)  # 加载数据
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=shuffle)  # 加载数据
    criterion = torch.nn.CrossEntropyLoss().to(device)
    if optimizer == 'SGD':
        optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)  # 优化器选用SGD
    elif optimizer == 'Adam':
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)  # 优化器选用Adam
    else:
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)  # 优化器默认选用Adam

    # 开始训练
    loss_epochs = []  # 所有轮次的损失
    accuracy_epochs = []  # 所有轮次的测试集精度
    for epoch in range(epochs):
        model.to(device).train()  # 训练模式
        loss_epoch = []  # 单轮的损失
        for batch_idx, (data, label) in enumerate(train_loader):
            data, label = data.to(device), label.to(device)  # 把数据送入device
            optimizer.zero_grad()  # 重置优化器
            output = model(data)  # 数据前向传递
            loss = criterion(output, label)  # 计算损失
            loss_epoch.append(loss.item())  # 加入当前损失
            loss.backward()  # 损失反向传播
            optimizer.step()  # 优化器优化
            if (batch_idx + 1) % 100 == 0:  # 输出
                accuracy = torch.mean((torch.max(output, dim=1)[1] == label).float())  # 计算准确度
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.4f}\tAccuracy: {:.2f}%'.format(
                    epoch + 1, batch_idx + 1, len(train_loader), 100. * (batch_idx + 1) / len(train_loader),
                    loss.item(), 100. * accuracy.item()))
        loss_epochs.append(loss_epoch)  # 保存loss
        if evaluate_mode:
            accuracy_epochs.append(evaluate(model, test_loader, device))  # 在测试集上测试
        print('--------------------------------------------------------------------')
        sys.stdout.flush()

    return loss_epochs, accuracy_epochs


def save(model: torch.nn.Module, save_path: str, name: str) -> None:
    if save_path.endswith(os.sep):
        filename = save_path + name + '.pth'
    else:
        filename = save_path + os.sep + name + '.pth'
    pt_dict = {
        'state_dict': model.state_dict()
    }
    torch.save(pt_dict, filename)
