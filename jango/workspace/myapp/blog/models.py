from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    img_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) :
        return self.title


class AboutUs(models.Model):
    content = models.TextField()

# class Edit(models.Model):
#     content = models.TextField()

class tb1_Authentication(models.Model):
    Empcode = models.IntegerField()
    username = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=50,default='')
    is_active =  models.IntegerField(null=True)

    def __str__(self):
        return self.username
    
    