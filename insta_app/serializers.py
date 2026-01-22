from rest_framework import serializers
from .models import (UserProfile, Post, Comment, Follow, PostContent,
                     PostLike, CommentLike)
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# ========== АУТЕНТИФИКАЦИЯ ==========
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'password', 'bio', 'user_image', 'is_official']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            user_image=validated_data.get('user_image', None),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Неверные учетные данные")

        refresh = RefreshToken.for_user(user)

        return {
            'user': user,
            'username': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


# ========== ПОЛЬЗОВАТЕЛИ ==========
class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'user_image', 'is_official', 'bio']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'bio', 'user_image', 'is_official',
                  'user_link', 'date_registered', 'followers_count',
                  'following_count', 'posts_count']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.followings.count()

    def get_posts_count(self, obj):
        return Post.objects.filter(user=obj).count()


# ========== ПОДПИСКИ ==========
class FollowSerializer(serializers.ModelSerializer):
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    following_username = serializers.CharField(source='following.username', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'follower_username',
                  'following_username', 'create_date']
        read_only_fields = ['create_date']


# ========== КОНТЕНТ ПОСТОВ ==========
class PostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ['id', 'post', 'content']


# ========== КОММЕНТАРИИ ==========
class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_image = serializers.ImageField(source='user.user_image', read_only=True)
    subcomments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'user_username', 'user_image',
                  'text', 'parent', 'created_date', 'subcomments']
        read_only_fields = ['created_date']

    def get_subcomments(self, obj):
        # Рекурсивно получаем подкомментарии
        if obj.subcomments.exists():
            return CommentSerializer(obj.subcomments.all(), many=True).data
        return []


# ========== ПОСТЫ ==========
class PostListSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    first_content = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'description', 'hashtag', 'created_date',
                  'likes_count', 'comments_count', 'first_content']

    def get_likes_count(self, obj):
        return PostLike.objects.filter(post=obj, like=True).count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_first_content(self, obj):
        # Получаем первый контент поста (картинку/видео)
        first = PostContent.objects.filter(post=obj).first()
        if first:
            return PostContentSerializer(first).data
        return None


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer(read_only=True)
    contents = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'description', 'hashtag', 'created_date',
                  'contents', 'comments', 'likes_count', 'is_liked']

    def get_contents(self, obj):
        contents = PostContent.objects.filter(post=obj)
        return PostContentSerializer(contents, many=True).data

    def get_comments(self, obj):
        # Возвращаем только главные комментарии (без родителя)
        comments = obj.comments.filter(parent__isnull=True).order_by('-created_date')
        return CommentSerializer(comments, many=True).data

    def get_likes_count(self, obj):
        return PostLike.objects.filter(post=obj, like=True).count()

    def get_is_liked(self, obj):
        # Проверяем, лайкнул ли текущий пользователь этот пост
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=request.user, like=True).exists()
        return False


# ========== ЛАЙКИ ==========
class PostLikeSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'post', 'user', 'user_username', 'like']


class CommentLikeSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CommentLike
        fields = ['id', 'comment', 'user', 'user_username', 'like']