#!/usr/bin/python3

"""
# -*- coding: utf-8 -*-

# @Time     : 2021/7/4 21:08
# @File     : train.py

"""
import torch

from torch.utils.data import DataLoader


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
