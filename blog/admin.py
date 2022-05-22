from django.contrib import admin
from .models import Post, Category, Tag, Comment
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):  # slug 자동 생성용
    prepopulated_fields = {'slug' : ('name', )}
    list_display = ['id','name']


class TagAdmin(admin.ModelAdmin):   # slug 자동 생성용
    prepopulated_fields = {'slug' : ('name', )}
    list_display = ['id','name']


class PostAdmin(admin.ModelAdmin):
    list_display = ['id','category','title','author','created']
    list_filter = ['created', 'author']
    search_fields = ['title','content', 'created', 'category__name']



admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
