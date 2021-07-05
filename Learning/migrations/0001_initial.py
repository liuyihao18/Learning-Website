# Generated by Django 3.2.5 on 2021-07-05 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelInfo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=64)),
                ('optimizer', models.CharField(max_length=64)),
                ('learning_rate', models.FloatField()),
                ('batch_size', models.IntegerField()),
                ('epochs', models.IntegerField()),
                ('task', models.CharField(max_length=64)),
                ('person', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=64)),
            ],
        ),
    ]
