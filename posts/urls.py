from django.urls import path
from . import views as posts_views
import posts

urlpatterns = [
    path('',posts_views.index,name="posts"),
    path('create/',posts_views.create, name="create"),
    path('createcategory/', posts_views.createcategory, name="createcategory"),
    path('<str:slug>/update/', posts_views.update, name="update"),
    path('my_posts/', posts_views.my_posts, name="my_posts"),
    path('my_categories/', posts_views.my_categories, name="my_categories"),
    path('delete/', posts_views.delete, name='delete'),
    path('postofcategory/<str:category>/', posts_views.postofcategory, name="postofcategory"),
    path('category/<str:slug>',posts_views.category,name="category"),
    path('<str:slug>/',posts_views.post,name="post")
    
]

