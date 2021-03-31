from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group
USER = get_user_model()


class CacheCaseTest(TestCase):
    """Тестирование функции кэша"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = USER.objects.create_user(username='TestUser')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Название группы',
            slug='test',
            description='Описание группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=cls.user,
        )

    def test_cache_index(self):
        """Тестирование функции кэша на главной странице"""

        response = self.authorized_client.get(reverse('index'))
        form_data = {
            'text': 'Новый пост',
            'group': self.group.id,
        }
        self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )

        self.assertNotContains(response, 'Новый пост')
