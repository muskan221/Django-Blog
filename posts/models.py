import os
import datetime

from django.db import models
from django.db.models.expressions import Value
from django.utils.text import slugify
from django.contrib.auth.models import User
from posts.manager import PostManager
from django.conf import settings

# Create your models here.

class Category(models.Model):
    
    name = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(default='',editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        value=slugify(self.name)
        self.slug=value
        super().save(*args, **kwargs)

    def __str__(self) -> str:# To properly view the names of categories
        return self.name

    class Meta:
        db_table="posts_categories"
        verbose_name_plural = "Categories" #because in admin page spelling of categories was wrong 

class Post(models.Model):

    def generate_cover_pic_path(self, filename):

        if filename != settings.DEFAULT_PIC:
            base_filename, file_extension = os.path.splitext(filename) #to break filename into its name and extension
             #and to get file name and its extension
            current_time_str = datetime.datetime.now().strftime
            ('%d-%m-%Y_%I:%M:%S,%f')
            filename = (f'{base_filename}_{current_time_str}{file_extension}')
            return f'post_pics/{filename}'

    title = models.CharField(max_length=250, unique=True)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(default='', editable=False, max_length=500)
    cover_pic = models.ImageField(default = settings.DEFAULT_PIC, upload_to = generate_cover_pic_path)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateField(null=True, blank=True)
    objects = PostManager()

    def save(self, *args, **kwargs):
        value = slugify(self.title)
        self.slug = value
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:# categories ka naam aache sedikhna chaye
        return self.title

    class Meta:
        db_table = "posts_posts"
