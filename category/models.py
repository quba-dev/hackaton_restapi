from django.db import models

class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True, default="garbage")
    # parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    # class Meta:
    #     verbose_name = 'category'
    #     verbose_name_plural = 'categories'