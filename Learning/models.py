from django.db import models


# Create your models here.
class ModelInfo(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    model = models.CharField(max_length=64)
    optimizer = models.CharField(max_length=64)
    learning_rate = models.FloatField()
    batch_size = models.IntegerField()
    epochs = models.IntegerField()
    task = models.CharField(max_length=64)
    person = models.CharField(max_length=64)
    begin_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(auto_created=True, null=True)
    state = models.CharField(max_length=64)
