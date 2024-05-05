from django.contrib import admin
from .models import Post, Response, likedPost

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created')
    list_filter = ('category', 'created')

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('author', 'parent_post', 'created','status')
    list_filter = ('author', 'created')

@admin.register(likedPost)
class likedPostAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created')
    list_filter = ('post', 'user', 'created')
    