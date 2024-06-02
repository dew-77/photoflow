from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='posts', verbose_name='Пользователь'
    )
    image = models.ImageField(
        upload_to='posts/', verbose_name='Изображение'
    )
    caption = models.TextField(blank=True, verbose_name='Подпись')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    def __str__(self):
        return f'Пост {self.user.username} от {self.created_at}'

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'публикации'


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments', verbose_name='Пользователь'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name='comments', verbose_name='Публикация'
    )
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    def __str__(self):
        return f'Комментарий: {self.user.username} - {self.post.id}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'комментарии'


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='likes', verbose_name='Пользователь'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name='likes', verbose_name='Публикация'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    def __str__(self):
        return f'{self.user.username} - {self.post.id}'

    class Meta:
        verbose_name = 'Отметка "нравится"'
        verbose_name_plural = 'отметки "нравится"'


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following', verbose_name='Кто подписан'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='followers', verbose_name='На кого подписан'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'Подписка'
        verbose_name_plural = 'подписки'

    def __str__(self):
        return f'Саб {self.follower.username} на {self.following.username}'


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.created_at}"
