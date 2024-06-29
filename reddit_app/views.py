from rest_framework import viewsets, generics
from .models import Subreddit, Post, Comment, Upvote, Subscription
from .serializers import SubredditSerializer, PostSerializer, CommentSerializer, UpvoteSerializer, SubscriptionSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import SubredditForm, PostForm, CommentForm

def index(request):
    return render(request, 'reddit_app/index.html')

@login_required
def user_profile(request):
    user = request.user
    subscribed_subreddits = Subscription.objects.filter(user=user)
    upvotes = Upvote.objects.filter(user=user)
    return render(request, 'reddit_app/profile.html', {
        'subscribed_subreddits': subscribed_subreddits,
        'upvotes': upvotes,
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'reddit_app/register.html', {'form': form})


def subreddit_list(request):
    subreddits = Subreddit.objects.all()
    return render(request, 'reddit_app/subreddit_list.html', {'subreddits': subreddits})

def subreddit_create(request):
    if request.method == 'POST':
        form = SubredditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subreddit_list')
    else:
        form = SubredditForm()
    return render(request, 'reddit_app/subreddit_create.html', {'form': form})

def post_list(request, subreddit_id):
    subreddit = Subreddit.objects.get(id=subreddit_id)
    posts = Post.objects.filter(subreddit=subreddit)
    return render(request, 'reddit_app/post_list.html', {'subreddit': subreddit, 'posts': posts})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'reddit_app/post_detail.html', {'post': post, 'comments': comments})

def post_create(request, subreddit_id):
    subreddit = Subreddit.objects.get(id=subreddit_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.subreddit = subreddit
            post.user = request.user
            post.save()
            return redirect('post_list', subreddit_id=subreddit_id)
    else:
        form = PostForm()
    return render(request, 'reddit_app/post_create.html', {'form': form})

def comment_create(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'reddit_app/comment_create.html', {'form': form})

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class SubredditViewSet(viewsets.ModelViewSet):
    queryset = Subreddit.objects.all()
    serializer_class = SubredditSerializer

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        subreddit = self.get_object()
        posts = Post.objects.filter(subreddit=subreddit).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        subreddit_id = self.kwargs.get('subreddit_id')
        if subreddit_id:
            return Post.objects.filter(subreddit_id=subreddit_id).order_by('-created_at')
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UpvoteViewSet(viewsets.ModelViewSet):
    queryset = Upvote.objects.all()
    serializer_class = UpvoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserProfileView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        subscribed_subreddits = Subscription.objects.filter(user=user)
        upvotes = Upvote.objects.filter(user=user)
        return Response({
            'subscribed_subreddits': SubredditSerializer(subscribed_subreddits, many=True).data,
            'upvotes': UpvoteSerializer(upvotes, many=True).data,
        })
    
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
