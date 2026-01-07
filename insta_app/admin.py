from django.contrib import admin
from .models import (UserProfile, Follow, Post, PostContent,
                     PostLike, Comment, CommentLike)


class FollowingInline(admin.TabularInline):
    model = Follow
    fk_name = 'following'
    verbose_name = 'Подписчик'
    verbose_name_plural = 'Подписчики'
    extra = 1

class FollowerInline(admin.TabularInline):
    model = Follow
    fk_name = 'follower'
    verbose_name = 'Подписка'
    verbose_name_plural = 'Подписки'
    extra = 1

class PostContentInline(admin.TabularInline):
    model = PostContent
    extra = 1

class PostLikeInline(admin.TabularInline):
    model = PostLike
    extra = 1

class CommentLikeInline(admin.TabularInline):
    model = CommentLike
    extra = 1

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [FollowingInline, FollowerInline]

class PostAdmin(admin.ModelAdmin):
    inlines = [PostContentInline, PostLikeInline]

class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentLikeInline]

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)