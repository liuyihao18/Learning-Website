import math
import datetime
import os
import re

from django.utils import timezone

from . import constants
from . import models

tz = datetime.timezone(datetime.timedelta(hours=+8))


# 把秒转化为时分秒
def change_to_hours_minutes_seconds(seconds: int) -> str:
    hours = int(seconds / 3600)
    minutes = int(seconds / 60) % 60
    seconds = seconds % 60
    return str(hours).zfill(2) + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2)


# 把obj中需要用到的提取出来
def change(obj):
    return {
        'id': obj.id,
        'task': obj.task,
        'person': obj.person,
        'add_time': obj.add_time.astimezone(tz).strftime(constants.time_pattern),
        'during_time': (
                (obj.finish_time and
                 change_to_hours_minutes_seconds((obj.finish_time - obj.add_time).seconds)) or
                (not obj.finish_time and
                 change_to_hours_minutes_seconds((timezone.now() - obj.add_time).seconds))),
        'finish_time': (obj.finish_time and obj.finish_time.astimezone(tz).strftime(constants.time_pattern)) or
                       (not obj.finish_time and '-------------------'),
        'raw_state': obj.state,
        'state': constants.translate[obj.state],
    }


# 获取任务列表的内容
def get_task_list_context(page):
    objs = models.ModelInfo.objects.all().order_by('-id')  # 增加'-'表示逆序
    max_page = max(math.ceil(objs.count() / constants.page_size), 1)  # 最大页数
    if page < 1:
        return {'redirect': '/result/1/'}  # 重定向
    if page > max_page:
        return {'redirect': '/result/' + str(max_page) + '/'}  # 重定向
    left = (page - 1) * constants.page_size  # 左索引
    right = min(page * constants.page_size, objs.count())  # 右索引
    objs = objs[left:right]  # 取出部分数据

    # 映射字典
    objs = list(map(change, objs))
    for i in range(len(objs)):
        objs[i]['item'] = left + i + 1

    # 左右切换
    left_enable = True
    left_url = '/result/' + str(max(1, page - 1)) + '/'
    right_enable = True
    right_url = '/result/' + str(min(max_page, page + 1)) + '/'
    if page == 1:
        left_enable = False
    if page == max_page:
        right_enable = False

    # 内容填充
    context = {
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


# 获取日志页面内容
def get_log_context(page, item):
    context = {
        'return_url': '/result/' + str(page) + '/',
        'col_names': constants.col_names,
        'now_page': page,
    }
    # 如果当前item不存在
    if not models.ModelInfo.objects.filter(id=item):
        context['not_found'] = True
    # 如果当前item存在
    else:
        # 补充对象信息
        obj = models.ModelInfo.objects.get(id=item)
        obj = change(obj)
        obj['item'] = '*'
        context['obj'] = obj
        # 获取log内容
        try:
            log = open(
                constants.extra_args['save_path'] + os.sep + constants.extra_args['log'] + os.sep + str(item) + ".log",
                'r')
            log_content = log.read()
            log.close()
        except FileNotFoundError:
            log_content = "Sorry, log is missing!"
        context['log_content'] = log_content
    return context


# 获取分析页面内容
def get_analysis_context(page, item):
    context = {
        'return_url': '/result/' + str(page) + '/',
        'item': item,
        'col_names': constants.col_names,
        'now_page': page,
        'loss_curve': constants.extra_args['loss_curve'],
        'accuracy_curve': constants.extra_args['accuracy_curve'],
    }
    if not models.ModelInfo.objects.filter(id=item):
        context['not_found'] = True
    else:
        # 补充对象信息
        obj = models.ModelInfo.objects.get(id=item)
        obj = change(obj)
        obj['item'] = '*'
        context['obj'] = obj
    return context


# 删除项目相关的文件
def delete(item):
    extension = {
        'model': '.pth',
        'log': '.log',
        'loss_curve': '.png',
        'accuracy_curve': '.png',
    }
    for sub_save_path in constants.sub_save_paths:
        try:
            os.remove(
                constants.extra_args['save_path'] + os.sep + constants.extra_args[sub_save_path] + os.sep + str(
                    item) +
                extension[sub_save_path])
        except FileNotFoundError:
            pass
        except PermissionError:
            pass


# 获取删除相关的内容
def get_delete_context(page, item):
    # 如果当前item存在
    if models.ModelInfo.objects.filter(id=item):
        # 删除数据库
        obj = models.ModelInfo.objects.get(id=item)
        obj.delete()
        # 删除存储
        delete(item)
    # 重定向
    context = {
        'redirect': '/result/' + str(page) + '/',
    }
    return context


# 获取清理相关的内容
def get_clean_context():
    # 正则表达式捕获
    reg = re.compile(r'^([0-9]*).\w*?$')
    # 需要清理的文件夹
    for sub_save_path in constants.sub_save_paths:
        # 需要清理的文件
        filenames = os.listdir(constants.extra_args['save_path'] + os.sep + sub_save_path)
        for filename in filenames:
            try:
                # 根据文件名获取数据库id
                item = int(reg.match(filename).group(1))
                # 判断是否存在于数据库，如果不存在，则删除残留文件
                if not models.ModelInfo.objects.filter(id=item):
                    os.remove(constants.extra_args['save_path'] + os.sep + sub_save_path + os.sep + filename)
            except ValueError:
                pass
            except FileNotFoundError:
                pass
            except PermissionError:
                pass
    # 重定向
    context = {
        'redirect': '/result/1/',
    }
    return context
