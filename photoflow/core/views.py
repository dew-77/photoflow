from django.db.models import Q
from django.views import generic
from .models import Post, Follow, Like, Comment
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


class PostListView(generic.ListView):
    model = Post
    template_name = 'core/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(caption__icontains=query) | Q(user__username__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']
        today = timezone.now().date()
        for post in posts:
            post.days_since_creation = (today - post.created_at.date()).days + 1
            if not self.request.user.is_anonymous:
                post.is_liked = Like.objects.filter(user=self.request.user, post=post).exists()
                post.is_followed = Follow.objects.filter(follower=self.request.user, following=post.user).exists()
        context['posts'] = posts
        context['comment_form'] = CommentForm()
        return context


class SubPostListView(generic.ListView):
    model = Post
    template_name = 'core/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            following_users = Follow.objects.filter(
                follower=self.request.user).values_list('following', flat=True)
            queryset = queryset.filter(user__in=following_users)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']
        today = timezone.now().date()
        for post in posts:
            post.days_since_creation = (today - post.created_at.date()).days + 1
            if not self.request.user.is_anonymous:
                post.is_liked = Like.objects.filter(user=self.request.user, post=post).exists()
                post.is_followed = Follow.objects.filter(follower=self.request.user,following=post.user).exists()
        context['posts'] = posts
        context['comment_form'] = CommentForm()
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'core/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'core/post_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'core/post_form.html'
    success_url = '/'


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'core/post_confirm_delete.html'
    success_url = '/'


class NotificationsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'core/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Получаем все посты текущего пользователя
        user_posts = Post.objects.filter(user=user)

        # Получаем все лайки и комментарии на посты текущего пользователя
        likes = Like.objects.filter(post__in=user_posts).select_related('user', 'post')
        comments = Comment.objects.filter(post__in=user_posts).select_related('user', 'post')

        # Добавляем атрибут `type` к каждому объекту
        for like in likes:
            like.type = 'like'
        for comment in comments:
            comment.type = 'comment'

        # Объединяем лайки и комментарии в один список и сортируем их по дате
        notifications = sorted(
            list(likes) + list(comments),
            key=lambda x: x.created_at,
            reverse=True
        )

        context['notifications'] = notifications

        return context