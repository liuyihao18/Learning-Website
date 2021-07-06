extra_args = {
    'num_classes': 10,
    'use_gpu': True,
    'data_path': 'data',
    'save_path': 'result',
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
    '持续时间',
    '完成时间',
    '任务状态',
    '操作',
]

translate = {
    'train': '训练中',
    'failure': '训练失败',
    'success': '训练完成',
}

page_size = 10

time_pattern = '%Y/%m/%d %H:%M'
during_time_pattern = '%H:%M'
