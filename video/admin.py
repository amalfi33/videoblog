from django.contrib import admin
from .models import Post, Category , Profile , Comment
# Register your models here.

class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, SlugAdmin)
admin.site.register(Category, SlugAdmin)
admin.site.register(Comment)
admin.site.register(Profile)