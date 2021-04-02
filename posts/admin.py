from django.contrib import admin
from .models import Group, Post, Comment, Follow


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Community page in the admin panel"""

    list_display = ('pk', 'title', 'description', 'slug')
    search_fields = ('title', 'description', 'slug',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Page of posts in the admin panel"""

    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group'
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Page of comments in the admin panel"""

    list_display = (
        'pk',
        'post',
        'author',
        'text',
        'created'
    )

    search_fields = ('text', 'author')
    list_filter = ('created',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Page of follow in the admin panel"""

    list_display = (
        'pk',
        'author',
        'user',
    )

    search_fields = ('author__username', 'user__username',)
