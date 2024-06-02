from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment, Like, Follow, User
from .serializers import FollowSerializer
from .serializers import PostSerializer, CommentSerializer, LikeSerializer


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AddCommentAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user, post_id=self.kwargs['pk'])


class LikePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(
            user=request.user, post=post
        )
        if not created:
            like.delete()
        return Response({'likes_count': post.likes.count()})


class AddFollowAPIView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        following_user = User.objects.get(pk=self.kwargs['pk'])
        serializer.save(follower=self.request.user, following=following_user)


class RemoveFollowAPIView(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        following_user = get_object_or_404(User, pk=self.kwargs['pk'])
        follow = get_object_or_404(Follow, follower=self.request.user, following=following_user)
        return follow
