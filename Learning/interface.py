import os
import threading

from django.utils import timezone

from Learning import constants
from Learning import models
from Learning.learning import main

lock = threading.Lock()


class Task(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self) -> None:
        lock.acquire()
        if not models.ModelInfo.objects.filter(id=self.id):
            lock.release()
            return
        obj = models.ModelInfo.objects.get(id=self.id)
        obj.state = 'train'
        obj.save()
        args = obj.__dict__
        args.update(constants.extra_args)
        try:
            main.instance(args)
        except Exception as e:
            with open(args['save_path'] + os.sep + 'log' + os.sep + str(self.id) + ".log", 'w') as f:
                f.write(str(type(e)) + ": " + str(e))
            if models.ModelInfo.objects.filter(id=self.id):
                obj.state = 'failure'
                obj.finish_time = timezone.now()
                obj.save()
            lock.release()
            return
        if models.ModelInfo.objects.filter(id=self.id):
            obj.state = 'success'
            obj.finish_time = timezone.now()
            obj.save()
        lock.release()
