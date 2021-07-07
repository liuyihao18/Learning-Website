import os

# 模型训练需要的额外参数
extra_args = {
    'num_classes': 10,
    'use_gpu': True,
    'data_path': 'Learning' + os.sep + 'learning' + os.sep + 'data',
    'save_path': 'Learning' + os.sep + 'static' + os.sep + 'Learning' + os.sep + 'assets',
    'model': 'model',
    'log': 'log',
    'loss_curve': 'loss_curve',
    'accuracy_curve': 'accuracy_curve',
}

# 需要保存的文件路径
sub_save_paths = ['loss_curve', 'accuracy_curve', 'log', 'model']

# 模型选项
model_options = [
    'LeNet',
]

# 优化器选项
optimizer_options = [
    'Adam',
    'SGD',
]

# 列名 - 英文
cols = [
    'id',
    'task',
    'person',
    'add_time',
    'during_time',
    'finish_time',
    'state',
    'operate',
]

# 列名 - 中文
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

# 对应
translate = {
    'wait': '等待中',
    'train': '训练中',
    'failure': '训练失败',
    'success': '训练完成',
}

# 分页数量
page_size = 10

# 时间模式
time_pattern = '%Y/%m/%d %H:%M'
during_time_pattern = '%H:%M'
