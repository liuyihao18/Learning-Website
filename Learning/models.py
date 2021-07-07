from django.db import models


# Create your models here.
class ModelInfo(models.Model):
    id = models.IntegerField(primary_key=True)  # id，主键
    model = models.CharField(max_length=64)  # 模型名称
    optimizer = models.CharField(max_length=64)  # 优化器
    learning_rate = models.FloatField()  # 学习率
    batch_size = models.IntegerField()  # 批次大小
    epochs = models.IntegerField()  # 训练轮次
    task = models.CharField(max_length=64)  # 任务名称
    person = models.CharField(max_length=64)  # 发起人
    add_time = models.DateTimeField(auto_now_add=True)  # 发起时间
    begin_time = models.DateTimeField(auto_created=True, null=True)  # 开始时间
    finish_time = models.DateTimeField(auto_created=True, null=True)  # 结束时间
    state = models.CharField(max_length=64)  # 状态
