# Generated by Django 3.1.4 on 2021-01-23 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20210123_2246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='commentor',
        ),
    ]
