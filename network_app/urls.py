from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('signup/', views.UserSignup.as_view(), name="signup"),
    path('login/', views.UserLogin.as_view(), name="login"),

    path('token/refresh/', jwt_views.TokenRefreshSlidingView.as_view(), name='token_refresh'),

    path('users/', views.NetworkUsers.as_view(), name="users"),
    path('users/<int:user_id>/activity/', views.UserActivity.as_view(), name="user_activity"),
    path('users/<int:user_id>/posts/', views.PostsByUser.as_view(), name="posts_by_user"),
    path('posts/', views.PostView.as_view(), name="create_user"),
    path('posts/<int:post_id>/like/', views.LikePost.as_view(), name="like_post"),
    path('posts/<int:post_id>/unlike/', views.UnlikePost.as_view(), name="unlike_post"),
    # path('analytics/', views.Analytics.as_view(), name="analytics"),
]
