from django.shortcuts import render ,  redirect
from .models import Post , Category , Profile , Comment , Like , View
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.contrib.auth import authenticate , login , logout
from django.urls import reverse
from .forms import RegisterForm
from .translit import translit
from random import randint
from django.utils import timezone
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
 

def index(request):
    posts = Post.objects.filter(published=True).order_by('-date')[:9]
    featureds = Post.objects.filter(featured = True).order_by('-date')[:5]
    categories = Category.objects.all()
    context = {'posts' : posts, 'featureds' : featureds, 'categories' : categories}
    return render(request, 'index.html', context)

def posts(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(published=True).order_by('-date')[:9]
    paginator = Paginator(posts, 20)
    page = request.GET.get('page')
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        posts = paginator.get_page(1)
    except EmptyPage:
        posts = paginator.get_page(paginator.num_pages)
    posts = paginator.get_page(page)
    context = {'posts' : posts, 'categories' : categories}
    return render(request, 'posts.html')

def post_detail(request, slug):
    post = Post.objects.get(slug__exact=slug)
    if request.user.is_authenticated:
        if not post.view_set.filter(user = request.user).exists():
            post.view_set.create(user = request.user)
        else:
            view = request.user.view_set.get(post=post)
            view.date = timezone.now()
            view.save()    
    return render(request, 'post_detail.html', {'post': post})

def category_detail(request, slug):
    category = Category.objects.get(slug__exact = slug)
    return render(request, 'category_detail.html', {'category':category})

def login_site(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            message = 'Username or password in incorrect'
            return render(request, 'login.html', {'message': message})
    return render(request, 'login.html')

def logout_site(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                profile = Profile()
                profile.user = user 
                profile.save()
                login(request, user)
                return redirect('index')
        else:
            form = RegisterForm()
        return render(request, 'register.html', {'form':form})
    return redirect('index')        
    
def comment(request,slug):
    post = Post.objects.get(slug__exact=slug)
    if request.method == 'POST':
        comment = Comment()
        comment.author = request.user
        comment.post = post
        comment.text = request.POST.get('text')
        if not comment.text:
             return redirect(reverse('post_detail_url', kwargs={'slug': slug}))
        comment.save()
        return redirect(reverse('post_detail_url', kwargs ={'slug': slug}))
    return redirect(reverse('post_detail_url', kwargs ={'slug': post.slug}))

def create_post(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        post = Post()
        post.title = request.POST.get('title')
        post.author = request.user
        new_slug = translit(request.POST.get('title'))
        if Post.objects.filter(slug__exact = new_slug).exists():
            post.slug = new_slug + '' + str(timezone.now().format('Y-m-d_H-i-s')) + '' + str(randint(1,100))
        else:
            post.slug = new_slug
        if request.FILES.get('preview', False) != False:
            myimage = request.FILES['preview']
            fsi = FileSystemStorage()
            filenameimage = fsi.save(myimage.name, myimage)
            post.preview = filenameimage
        if request.FILES.get('video', False) != False:
            myvideo = request.FILES['video']
            fsv = FileSystemStorage()
            filenamevideo = fsv.save(myvideo.name, myvideo)
            post.video = filenamevideo
        post.description = request.POST.get('description')
        post.save()
        category_ids = request.POST.getlist('categories[]')
        for id in category_ids:
            post.category.add(id)
        return redirect('index')
    return render(request, 'create_post.html', {'categories': categories })


#  <----Поиск---->
def search(request):
    query = request.GET.get('search')
    posts = Post.objects.filter(Q(title__iregex = query))
    content = {'posts': posts, 'query' : query }
    return render(request, 'search.html', content)

def profile(request, user_id):
    profile = Profile.objects.get(user_id__exact = request.user.id)
    return render(request, "profile.html", {'profile': profile})

def post_delete(request, slug):
    post = Post.objects.get(slug__exact=slug)
    post.delete()
    return redirect('index')    

    
def edit_post(request, slug):
    categories = Category.objects.all()
    post = Post.objects.get(slug__exact=slug)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.author = request.user
        new_slug = translit(request.POST.get('title'))
        post.slug = new_slug
        if request.FILES.get('preview', False) != False:
            myimage = request.FILES['preview']
            fsi = FileSystemStorage()
            filenameimage = fsi.save(myimage.name, myimage)
            post.preview = filenameimage
        if request.FILES.get('video', False) != False:
            myvideo = request.FILES['video']
            fsv = FileSystemStorage()
            filenamevideo = fsv.save(myvideo.name, myvideo)
            post.video = filenamevideo
        post.description = request.POST.get('description')
        post.save()
        category_ids = request.POST.getlist('categories[]')
        for id in category_ids:
            post.category.add(id)
        return redirect('index')
    return render(request, 'edit_post.html', {'categories': categories,'post':post })

def like(request, slug):
    post = Post.objects.get(slug__exact=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if not post.like_set.create(user = request.user).exists():
                post.like_set.create(user = request.user)
            else:
                like = request.user.like_set.get(post=post)
                like.delete()
        else:
            return redirect('login')
        return redirect(reverse('post_detail_url', kwargs={'slug':slug}))