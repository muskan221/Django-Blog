from django.contrib.auth.decorators import login_required
from .models import Category,Post
from .forms import CategoryForm, PostForm
import datetime
from django.shortcuts import get_object_or_404, render,HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import  BadRequest, PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def post(request,slug):
    #post = Post.query.filter(slug = slug).first()
    post  = get_object_or_404(Post, slug=slug)
    post.increment_views()
   
    #return HttpResponse(f"<h1> {post.title} </h1> <br> <p> {post.content}</p>")
    context = {
        'post':post,
    }
    return render(request, "post.html", context)

def category(request,slug):
    category  = get_object_or_404(Category, slug=slug)
    context = {
        'category':category
    }
    return render(request, "category.html", context)


def index(request):
    latest_posts = Post.query.all().order_by("-created_at")[:6]
    trending_posts = Post.query.all().order_by("-views")[:3]
    context = {
        'latest_posts': latest_posts,
        'trending_posts': trending_posts,
        'tab': 'dashboard',
    }

    return render(request, "index.html", context)

@login_required
def create(request): 

    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            post = form.save()
            messages.success(request, f"{post.title}  post created successfully")
            #return HttpResponse(post.title)
            return redirect("post", slug=post.slug)
        messages.error(request, f"Error while creating a post")
    else:
        form = PostForm()
        
    context = {
        'form' : form,
        'tab': 'create',
    }
    return render(request, "create.html", context)

def createcategory(request):
    
    if request.method == 'POST':
        form  = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect("category", slug=category.slug)
        
    else:
        form = CategoryForm()
        
    context = {                
        'form' : form,
        }
    return render(request, "createcategory.html", context)


@login_required
def update(request, slug):

    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        raise PermissionDenied()

    
    if request.method == 'POST':    
        form = PostForm(request.POST, request.FILES, instance=post) #request.FILES because after creating a post image was not visisble
        # form.instance.author = request.user
        if form.is_valid():
            # form.instance.author = request.user
            post = form.save()
            messages.success(request, f"{post.title}  post updated successfully ")
            #return HttpResponse(post.title)
            return redirect("post", slug=post.slug)
        messages.error(request, f"Error while updating a post")
    else:
        form = PostForm(instance=post)
        
    context = {
        'form' : form,
    }
    return render(request, "create.html", context)


@login_required
def delete(request):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=request.POST.get("slug", None))
        if request.user != post.author:
            raise PermissionDenied()
        
        post.deleted_at = datetime.datetime.now()
        post.save()
        messages.success(request, f"{post.title}  post Moved to Thrash")
        return redirect("my_posts")
    else:
        raise BadRequest()

@login_required
def trash(request):

    posts = Post.objects.filter(author=request.user).exclude(deleted_at=None)
    context ={
        'posts' : posts,
    }
    return render(request, "trash.html", context)

@login_required
def restore(request, slug):
    if request.method == 'GET':
        post = get_object_or_404(Post.objects, slug=slug)
        if request.user != post.author:
            raise PermissionDenied()

        post.deleted_at = None
        post.save()
        messages.success(request, f"{post.title} Restored")
        return redirect("my_posts")
    else:
        raise BadRequest()

@login_required
def permanent_delete(request):
    if request.method == 'POST':
        post = get_object_or_404(Post.objects, slug=request.POST.get("slug", None))
        if request.user != post.author:
            raise PermissionDenied()
        post.delete()
        messages.success(request, f"{post.title}  Post Deleted successfully")
        return redirect("my_posts")
    else:
        raise BadRequest()


@login_required
def my_posts(request):

    posts = Post.query.filter(author=request.user)
    paginator = Paginator(posts,4)
    # ek page pe 4 posts aane chaye
    is_paginated = paginator.num_pages > 1
    page = request.GET.get("page", 1)
    # agar url me kuch nhi likha page no= toh by default page 1 dikhayega
    if int(page) > paginator.num_pages:
        page = 1
    page_obj = paginator.page(page) 
    context ={
        'is_paginated':is_paginated,
         'page_obj':page_obj,
          'tab': 'my_posts',
    }
    return render(request, "my_posts.html", context)

def search(request):

    search = request.GET.get("search", "")
    posts = Post.query.filter(Q(title__icontains=search) | Q(content__icontains=search))
    if not posts:
        # posts -> collection
        messages.info(request, f"No Posts found for search result - {search}")
    paginator = Paginator(posts, 2)
    is_paginated = paginator.num_pages > 1
    page = request.GET.get("page", 1)
    if int(page) > paginator.num_pages:
        page = 1
    page_obj = paginator.page(page)
    context = {
        'search':search,
        'is_paginated': is_paginated,
        'page_obj':page_obj,
    }
    return render(request, "my_posts.html", context)
    

def my_categories(request):

    categories = Category.objects.all()
    context ={
        'categories' : categories 
    }
    return render(request, "my_categories.html", context)

def postofcategory(request, category):
    postofcategory = Post.objects.filter(category__name = category)
    context ={
         'postofcategory':postofcategory
    }
    return render(request, "postofcategory.html", context)









