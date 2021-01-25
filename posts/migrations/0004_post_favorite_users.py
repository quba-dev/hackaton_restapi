# Generated by Django 3.1.4 on 2021-01-24 10:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0003_remove_comment_commentor'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='favorite_users',
            field=models.ManyToManyField(related_name='favorite_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]