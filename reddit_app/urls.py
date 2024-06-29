from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubredditViewSet, PostViewSet, CommentViewSet, UpvoteViewSet, SubscriptionViewSet, UserProfileView, RegisterView
from . import views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'subreddits', SubredditViewSet)
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet)
router.register(r'upvotes', UpvoteViewSet)
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('subreddits/', views.subreddit_list, name='subreddit_list'),
    path('subreddits/create/', views.subreddit_create, name='subreddit_create'),
    path('subreddits/<int:subreddit_id>/posts/', views.post_list, name='post_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/create/<int:subreddit_id>/', views.post_create, name='post_create'),
    path('comments/create/<int:post_id>/', views.comment_create, name='comment_create'),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/user/profile/', UserProfileView.as_view({'get': 'list'}), name='user-profile'), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/subreddits/<int:subreddit_id>/posts/', PostViewSet.as_view({'get': 'list'}), name='subreddit-posts'),  
    path('api/posts/<int:post_id>/comments/', CommentViewSet.as_view({'get': 'list'}), name='post-comments'),
    path('login/', auth_views.LoginView.as_view(template_name='reddit_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.user_profile, name='profile'),
    path('register/', views.register, name='register'),
]
