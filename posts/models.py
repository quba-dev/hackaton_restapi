from django.db import models

from pikabu_api import settings
from user.models import CustomUser
from category.models import Category


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quba')
    video_url = models.URLField(blank=True, null=True)
    poster = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    video = models.FileField(upload_to='posts', blank=True, null=True)
    # favorite_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="favorite_posts")
    # favorite_users = models.ManyToManyField(CustomUser, related_name="favorite_posts")



    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.id}: {self.title} -> {self.title}'


class Vote(models.Model):
    voter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: {self.voter} -> {self.post}'


# class Comments(models.Model):
#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_comments')
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
#     text = models.CharField(max_length=1000)
#
#     def __str__(self):
#         return f'{self.author}:{self.text} to {self.post}'
#

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    # commentor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='commentor')
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.id} Comment by on {self.post}'

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


