from posts.models import Category, Post
from django.contrib import admin
from .models import Post,Category

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)