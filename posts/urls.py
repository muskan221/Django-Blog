from django.urls import path
from . import views as posts_views
import posts

urlpatterns = [
    path('<str:slug>/',posts_views.post,name="post"),
    path('',posts_views.index,name="posts"),
    path('create',posts_views.create, name="create"),
    path('createcategory', posts_views.createcategory, name="createcategory")
]