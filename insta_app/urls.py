from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    UserProfileListAPIView,
    UserProfileDetailAPIView,
    PostListAPIView,
    PostDetailAPIView,
    CommentViewSet,
    RegisterView,
    CustomLoginView,
    LogoutView,
    FollowViewSet,
    PostContentViewSet,
    PostLikeViewSet,
    CommentLikeViewSet,
)

router = SimpleRouter()

router.register(r'follow', FollowViewSet)
router.register(r'post_content', PostContentViewSet)
router.register(r'post_likes', PostLikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'comment_likes', CommentLikeViewSet)

urlpatterns = [
    path('', include(router.urls)),


    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),

    path('post/', PostListAPIView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
]