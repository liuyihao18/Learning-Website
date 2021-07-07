import os
import threading

from django.utils import timezone

from Learning import constants
from Learning import models
from Learning.learning import main
from Learning.logic import delete

lock = threading.Lock()


class Task(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self) -> None:
        # 获得锁
        lock.acquire()
        # 确认该任务当前是否存在
        if not models.ModelInfo.objects.filter(id=self.id):
            lock.release()
            return
        # 将状态设置为训练，并更新开始时间
        obj = models.ModelInfo.objects.get(id=self.id)
        obj.state = 'train'
        obj.begin_time = timezone.now()
        obj.save()
        # 配置参数
        args = obj.__dict__
        args['begin_time'] = obj.begin_time
        args.update(constants.extra_args)
        # 产生训练实例
        try:
            main.instance(args)
        except Exception as e:
            # 如果发生异常，则把异常写入日志
            with open(args['save_path'] + os.sep + 'log' + os.sep + str(self.id) + ".log", 'w') as f:
                f.write(str(type(e)) + ": " + str(e))
            # 再次确认该任务是否存在
            if models.ModelInfo.objects.filter(id=self.id):
                # 设置最终状态，并更新结束时间
                obj.state = 'failure'
                obj.finish_time = timezone.now()
                obj.save()
            # 如果不存在，删除相关文件
            else:
                delete(self.id)
            lock.release()
            return
        # 再次确认该任务是否存在
        if models.ModelInfo.objects.filter(id=self.id):
            # 设置最终状态，并更新结束时间
            obj.state = 'success'
            obj.finish_time = timezone.now()
            obj.save()
        # 如果不存在，删除相关文件
        else:
            delete(self.id)
        lock.release()
