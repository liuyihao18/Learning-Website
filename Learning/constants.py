import os

extra_args = {
    'num_classes': 10,
    'use_gpu': True,
    'data_path': 'Learning' + os.sep + 'learning' + os.sep + 'data',
    'save_path': 'Learning' + os.sep + 'static' + os.sep + 'Learning' + os.sep + 'assets',
    'log': 'log',
    'loss_curve': 'loss_curve',
    'accuracy_curve': 'accuracy_curve',
}

cols = [
    'id',
    'task',
    'person',
    'begin_time',
    'during_time',
    'finish_time',
    'state',
    'operate',
]

col_names = [
    '#',
    '任务名称',
    '发起人',
    '发起时间',
    '持续时长',
    '完成时间',
    '任务状态',
    '操作',
]

translate = {
    'wait': '等待中',
    'train': '训练中',
    'failure': '训练失败',
    'success': '训练完成',
}

page_size = 10

time_pattern = '%Y/%m/%d %H:%M'
during_time_pattern = '%H:%M'
