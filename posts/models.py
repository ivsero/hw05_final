from django.db import models
from django.contrib.auth import get_user_model


USER = get_user_model()


class Group(models.Model):
    """Community model"""
    title = models.CharField(
        'Название сообщества',
        max_length=200,
    )
    slug = models.SlugField(
        'Директория',
        unique=True
    )
    description = models.TextField(
        'Описание',
        null=True
    )

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Post model"""
    text = models.TextField(
        'Текст публикации',
        help_text='Напишите что-нибудь'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        USER,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Сообщество',
        on_delete=models.CASCADE,
        related_name='posts',
        blank=True,
        null=True,
        help_text='Укажите сообщество'
    )
    image = models.ImageField(
        verbose_name='Пикча',
        upload_to='posts/',
        blank=True,
        null=True,
        help_text='Загрузите изображение'
    )

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Comment model"""
    post = models.ForeignKey(
        Post,
        verbose_name='Комментарий',
        on_delete=models.CASCADE,
        related_name='Post'
    )
    author = models.ForeignKey(
        USER,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='author_comment'
    )
    text = models.TextField(
        'Ваш комментарий',
        help_text='Что скажете?'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:10]


class Follow(models.Model):
    """Follow model"""

    user = models.ForeignKey(
        USER,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower'
    )

    author = models.ForeignKey(
        USER,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
