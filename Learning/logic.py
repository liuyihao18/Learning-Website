import math
import datetime

from django.utils import timezone

from . import constants
from . import models


def get_table_context(page):
    objs = models.ModelInfo.objects.all().order_by('-id')  # 增加'-'表示逆序
    max_page = max(math.ceil(objs.count() / constants.page_size), 1)  # 最大页数
    if page < 1:
        return {'redirect': '/result/1/'}  # 重定向
    if page > max_page:
        return {'redirect': '/result/' + str(max_page) + '/'}  # 重定向
    left = (page - 1) * constants.page_size  # 左索引
    right = min(page * constants.page_size, objs.count())  # 右索引
    objs = objs[left:right]  # 取出部分数据
    tz = datetime.timezone(datetime.timedelta(hours=+8))

    # 把秒转化为时分秒
    def change_to_hours_minutes_seconds(seconds: int) -> str:
        hours = int(seconds / 3600)
        minutes = int(seconds / 60) % 60
        seconds = seconds % 60
        return str(hours).zfill(2) + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2)

    # 映射字典
    objs = list(map(lambda obj: {
        'id': obj.id,
        'task': obj.task,
        'person': obj.person,
        'begin_time': obj.begin_time.astimezone(tz).strftime(constants.time_pattern),
        'during_time': (
                (obj.finish_time and
                 change_to_hours_minutes_seconds((obj.finish_time - obj.begin_time).seconds)) or
                (not obj.finish_time and
                 change_to_hours_minutes_seconds((timezone.now() - obj.begin_time).seconds))),
        'finish_time': (obj.finish_time and obj.finish_time.astimezone(tz).strftime(constants.time_pattern)) or
                       (not obj.finish_time and '-------------------'),
        'raw_state': obj.state,
        'state': constants.translate[obj.state],
    }, objs))

    # 左右切换
    left_enable = True
    left_url = '/result/' + str(min(1, page - 1)) + '/'
    right_enable = True
    right_url = '/result/' + str(max(max_page, page + 1)) + '/'
    if page == 1:
        left_enable = False
    if page == max_page:
        right_enable = False

    # 内容填充
    context = {
        'active': 'result',
        'cols': constants.cols,
        'col_names': constants.col_names,
        'objs': objs,
        'now_page': page,
        'total_page': max_page,
        'left_enable': left_enable,
        'left_url': left_url,
        'right_enable': right_enable,
        'right_url': right_url,
    }
    return context


def get_log_context(page, item):
    context = {
        'return_url': '/result/' + str(page) + '/',
    }
    return context


def get_result_context(page, item):
    context = {
        'return_url': '/result/' + str(page) + '/',
    }
    return context
