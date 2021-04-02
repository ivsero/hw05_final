from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group


USER = get_user_model()


class PostCreateFormTests(TestCase):
    """Тестирование отправки форм"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = USER.objects.create_user(username='TestUser')
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

    def test_create_new_post(self):
        """Валидная форма создает новую запись в Post."""
        posts_count = Post.objects.count()

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
            'image': uploaded,
        }

        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), posts_count + 1)


class PostEditFormTests(TestCase):
    """Тестирование формы редактирования"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = USER.objects.create_user(username='TestUser')
        cls.user2 = USER.objects.create_user(username='TestUser2')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.authorized_client2 = Client()
        cls.authorized_client2.force_login(cls.user2)
        cls.group = Group.objects.create(
            title='Название группы',
            slug='test',
            description='Описание группы',
        )

    def test_edit_post_for_authorized_client(self):
        """Проверка отображения отредактированного
        поста для авторизованного пользователя"""
        post = Post.objects.create(
            text='Старый текст',
            group=self.group,
            author=self.user,
        )

        posts_count = Post.objects.count()

        form_fields = {
            'text': 'Новый пост',
            'author': self.user
        }
        self.authorized_client.post(
            reverse(
                'post_edit', kwargs={'username': self.user, 'post_id': post.id}
            ), data=form_fields, follow=True
        )
        edited_post = Post.objects.get(id__exact=post.id)

        self.assertEqual(edited_post.text, 'Новый пост')
        self.assertEqual(Post.objects.count(), posts_count)

    def test_edit_post_for_guest_client(self):
        """Проверка отображения отредактированного
        поста для неавторизованного пользователя"""
        post = Post.objects.create(
            text='Старый текст',
            group=self.group,
            author=self.user,
        )
        form_fields = {
            'text': 'Новый пост',
            'author': self.user
        }
        self.guest_client.post(
            reverse(
                'post_edit', kwargs={'username': self.user, 'post_id': post.id}
            ), data=form_fields, follow=True
        )
        edited_post = Post.objects.get(id__exact=post.id)
        self.assertNotEqual(edited_post.text, 'Новый пост')

    def test_edit_post_for_user(self):
        """Проверка отображения отредактированного
        поста для пользователя"""

        post = Post.objects.create(
            text='Старый текст',
            group=self.group,
            author=self.user,
        )

        posts_count = Post.objects.count()

        form_fields = {
            'text': 'Новый пост',
            'author': self.user
        }
        self.authorized_client2.post(
            reverse(
                'post_edit', kwargs={'username': self.user, 'post_id': post.id}
            ), data=form_fields, follow=True
        )
        edited_post = Post.objects.get(id__exact=post.id)

        self.assertNotEqual(edited_post.text, 'Новый пост')
        self.assertEqual(Post.objects.count(), posts_count)
