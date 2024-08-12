from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    img_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
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
    


    