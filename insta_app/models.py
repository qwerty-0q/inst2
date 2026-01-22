from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    bio = models.TextField(null=True,blank=True)
    user_image = models.ImageField(null=True,blank=True)
    is_official = models.BooleanField(default=False)
    user_link = models.URLField(null=True,blank=True)
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'@{self.username}'

class Follow(models.Model):
    following = models.ForeignKey(UserProfile,related_name='followings', on_delete=models.CASCADE)
    follower = models.ForeignKey(UserProfile, related_name='followers', on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} > {self.following.username}'

    class Meta:
        unique_together = ('follower', 'following')


class Post(models.Model):
    description = models.TextField(null=True,blank=True)
    hashtag = models.CharField(max_length=100,null=True,blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.description[:10]} ({self.created_date})'


class PostContent(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    content = models.FileField(upload_to='posts/')

    def __str__(self):
        return f'Content for Post {self.post.id}'


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'Post {self.post.id} - {self.like}'


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='subcomments')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.post.id}: {self.user.username} - {self.text[:30]}'


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment {self.comment.id} - {self.like}'

    class Meta:
        unique_together = ('comment', 'user')


