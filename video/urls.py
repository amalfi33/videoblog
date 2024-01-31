from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts , name = 'posts'),
    path('posts/<slug:slug>/', views.post_detail , name = 'post_detail_url'),
    path('category/<slug:slug>/', views.category_detail , name = 'category_detail_url'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.login_site, name='login_site'),
    path('logout/', views.logout_site, name='logout_site'),
    path('post_detail/<slug:slug>/comment/', views.comment, name='comment'),
    path('search/', views.search, name='search'),
    path('profile/<slug:user_id>/', views.profile, name = 'profile'),
    path('create_post/', views.create_post, name = 'create_post'),
    path('post_delete/<slug:slug>', views.post_delete, name = 'post_delete'),
    path('edit_post/<slug:slug>', views.edit_post, name = 'edit_post'),   
    path('posts/<slug:slug>/like/', views.like, name = 'like'),
]