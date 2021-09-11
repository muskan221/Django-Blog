from django.urls import path
from . import views as posts_views
import posts

urlpatterns = [
    path('',posts_views.index,name="posts"),
    path('create/',posts_views.create, name="create"),
    path('createcategory/', posts_views.createcategory, name="createcategory"),
    path('<str:slug>/update/', posts_views.update, name="update"),
    path('my_posts/', posts_views.my_posts, name="my_posts"),
    path('delete/', posts_views.delete, name='delete'),
    path('<str:slug>/',posts_views.post,name="post")
]

