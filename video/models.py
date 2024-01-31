from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class Post(models.Model):
    author =  models.ForeignKey(User, on_delete=models.CASCADE, null = True , blank = True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to = 'post_previews/')
    video = models.FileField(upload_to='post_videos/')
    date = models.DateTimeField(default = timezone.now)
    published = models.BooleanField(default = False)
    category = models.ManyToManyField('Category')
    featured = models.BooleanField(default= False)
    slug = models.SlugField(unique = True)

    class  Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return self.title
    
    def get_link(self):
        return reverse('post_detail_url', kwargs= {'slug': self.slug})
    
class Category(models.Model):
    title = models.CharField(max_length = 255)
    slug = models.SlugField(unique = True)

    class Meta:
        verbose_name = 'Категория'  
        verbose_name_plural = 'Категории'
        
    def __str__(self):
        return self.title

    def get_link(self):
        return reverse('category_detail_url', kwargs= {'slug': self.slug})
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    avatar = models.ImageField(upload_to= 'user_avatars/', null= True)
    banner = models.ImageField(upload_to='user_banners/', null= True)
    birth_day = models.DateField(null = True)
    description = models.TextField(null= True, blank= True)

    class Meta:
        verbose_name = 'Профиль'  
        verbose_name_plural = 'Профили'
        
    def __str__(self):
        return self.user.username

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default = timezone.now)

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.author.username + self.text
    
class View(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null= True, blank=True)
    date = models.DateTimeField(default= timezone.now)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null= True, blank=True)
    date = models.DateTimeField(default= timezone.now)
    
    

        




        