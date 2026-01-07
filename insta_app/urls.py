from .views import (UserProfileListAPIView, UserProfileDetailAPIView,
                    PostListAPIView, PostDetailAPIView, CommentViewSet,
                    RegisterView, CustomLoginView, LogoutView)
from django.urls import path, include
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register(r'comment', CommentViewSet)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_list'),
    path('login/', CustomLoginView.as_view(), name='login_list'),
    path('logout/', LogoutView.as_view(), name='logout_list'),
    path('', include(router.urls)),

    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('post/', PostListAPIView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail')
]