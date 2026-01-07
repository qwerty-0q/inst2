from rest_framework import serializers
from .models import (UserProfile, Follow, Post, PostContent,
                     PostLike, Comment, CommentLike)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileListSerializer(serializers.ModelSerializer):
    followings = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user_image', 'followings',
                  'followers', 'posts', 'is_official']

    def followings(self, obj):
        return obj.followings

    def followers(self, obj):
        return obj.followers

    def posts(self, obj):
        return obj.posts


class UserProfileDetailSerializer(serializers.ModelSerializer):
    followings = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    date_registered = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = UserProfile
        fields = ['id', 'user_image', 'followings',
                  'followers', 'posts', 'is_official',
                  'phone_number', 'bio', 'date_registered']

    def followings(self, obj):
        return obj.followings

    def followers(self, obj):
        return obj.followers

    def posts(self, obj):
        return obj.posts


class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['following', 'follower']


class PostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ['id', 'post_content']


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    content_post = PostContentSerializer(many=True, read_only=True)
    user = UserProfileNameSerializer()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'content_post', 'likes',
                  'hashtag', 'description', 'created_date']

    def likes(self, obj):
        return obj.likes


class CommentLikeSerializer(serializers.ModelSerializer):
    comment_likes = serializers.SerializerMethodField()

    class Meta:
        model = CommentLike
        fields = ['id', 'comment_likes']

    def comment_likes(self, obj):
        return obj.comment_likes


class CommentSerializer(serializers.ModelSerializer):
    comment_likes = serializers.SerializerMethodField()
    user = UserProfileNameSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'parent', 'created_date',
                  'comment_likes']

    def comment_likes(self, obj):
        return obj.comment_likes


class PostDetailSerializer(serializers.ModelSerializer):
    content_post = PostContentSerializer(many=True, read_only=True)
    post_comment = CommentSerializer(many=True, read_only=True)
    user = UserProfileNameSerializer()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'content_post', 'likes',
                  'hashtag', 'description', 'created_date', 'post_comment']

    def likes(self, obj):
        return obj.likes