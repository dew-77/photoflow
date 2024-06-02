from django.urls import path
from . import views

urlpatterns = [
    path('myfeed/', views.SubPostListView.as_view(), name='post_discover'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('notifications/', views.NotificationsView.as_view(), name='notifications'),
    path('messages/', views.MessagesView.as_view(), name='messages'),
]
