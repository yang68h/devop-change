# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-06 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opman', '0006_hostxlsx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostxlsx',
            name='date',
            field=models.DateField(verbose_name='日期'),
        ),
        migrations.AlterField(
            model_name='hostxlsx',
            name='filename',
            field=models.FileField(upload_to='./upload/xlsx', verbose_name='选择文件'),
        ),
    ]
