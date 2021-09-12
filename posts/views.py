from django.contrib.auth.decorators import login_required
from .models import Category,Post
from .forms import CategoryForm, PostForm
import datetime
from django.shortcuts import get_object_or_404, render,HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import  BadRequest, PermissionDenied

# Create your views here.
def post(request,slug):
    #post = Post.objects.filter(slug = slug).first()
    post  = get_object_or_404(Post, slug=slug)
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
    post = Post.objects.all()
    print(post)
    return render(request, "index.html")

@login_required
def create(request): 

    if request.method == 'POST':

        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            post = form.save()
            #return HttpResponse(post.title)
            return redirect("post", slug=post.slug)
        
    else:
        form = PostForm()
        
    context = {
        'form' : form,
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
        form = PostForm(request.POST, instance=post)
        # form.instance.author = request.user
        if form.is_valid():
            # form.instance.author = request.user
            post = form.save()
            #return HttpResponse(post.title)
            return redirect("post", slug=post.slug)
        
    else:
        form = PostForm(instance=post)
        
    context = {
        'form' : form,
    }
    return render(request, "create.html", context)


@login_required
def delete(request):
    print("->", request.POST)
    if request.method == 'POST':
        print("->", request.POST)
        post = get_object_or_404(Post, slug=request.POST.get("slug", None))
        if request.user != post.author:
            raise PermissionDenied()
        
        post.deleted_at = datetime.datetime.now()
        post.save()
        return redirect("my_posts")
    else:
        raise BadRequest()
     

@login_required
def my_posts(request):

    posts = Post.objects.filter(author=request.user)
    context ={
        'posts' : posts,
    }
    return render(request, "my_posts.html", context)








