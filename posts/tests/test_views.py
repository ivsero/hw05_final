from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group
USER = get_user_model()


class PostsPagesTests(TestCase):
    """Тестирование функций постов"""
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
            image='image/gif'
        )

    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'index.html': reverse('index'),
            'group.html': (
                reverse(
                    'group_posts',
                    kwargs={'slug': 'test'}
                )),
            'post_form.html': (
                reverse(
                    'post_edit',
                    kwargs={'username': self.user.username,
                            'post_id': self.post.id, }
                )),
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template,
                                        'Тест не прошел'
                                        )

    def test_home_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('index'))
        post_object = response.context['page'][0]
        post_author_0 = post_object.author
        post_pub_date_0 = post_object.pub_date
        post_text_0 = post_object.text
        post_img_0 = post_object.image

        self.assertEqual(post_author_0, PostsPagesTests.post.author,
                         'Тест не прошел, автора нет в контексте'
                         )
        self.assertEqual(post_pub_date_0, PostsPagesTests.post.pub_date,
                         'Тест не прошел, даты нет в контексте'
                         )
        self.assertEqual(post_text_0, PostsPagesTests.post.text,
                         'Тест не прошел, текста нет в контексте'
                         )
        self.assertEqual(post_img_0, PostsPagesTests.post.image,
                         'Тест не прошел, текста нет в контексте'
                         )

    def test_gorup_page_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test'})
        )

        self.assertEqual(response.context['group'].title,
                         'Название группы',
                         'Тест не прошел, названия нет в контексте'
                         )
        self.assertEqual(response.context['group'].description,
                         'Описание группы',
                         'Тест не прошел, описания нет в контексте'
                         )
        self.assertEqual(response.context['group'].slug, 'test',
                         'Тест не прошел, группы нет в контексте'
                         )

    def test_create_or_edit_post_page_shows_correct_context(self):
        """Шаблон new сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(
                    form_field, expected,
                    'Тест не прошел, текст не соответствует ожиданию'
                )

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('profile', kwargs={'username': self.user.username, }))
        test_user_profile = response.context['user_profile']
        post_object = response.context['page'][0]
        post_author_0 = post_object.author
        post_pub_date_0 = post_object.pub_date
        post_text_0 = post_object.text
        post_img_0 = post_object.image

        self.assertEqual(test_user_profile, self.user)
        self.assertEqual(post_object, self.post)
        self.assertEqual(post_author_0, PostsPagesTests.post.author,
                         'Тест не прошел, автора нет в контексте'
                         )
        self.assertEqual(post_pub_date_0, PostsPagesTests.post.pub_date,
                         'Тест не прошел, даты нет в контексте'
                         )
        self.assertEqual(post_text_0, PostsPagesTests.post.text,
                         'Тест не прошел, текста нет в контексте'
                         )
        self.assertEqual(post_img_0, PostsPagesTests.post.image,
                         'Тест не прошел, текста нет в контексте'
                         )

    def test_post_page_show_correct_context(self):
        """Шаблон post сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('post', kwargs={
                'username': self.user.username,
                'post_id': self.post.id,
            }
            ))
        post_object = response.context['post']
        post_author_0 = post_object.author
        post_pub_date_0 = post_object.pub_date
        post_text_0 = post_object.text
        post_img_0 = post_object.image

        self.assertEqual(post_author_0, PostsPagesTests.post.author,
                         'Тест не прошел, автора нет в контексте'
                         )
        self.assertEqual(post_pub_date_0, PostsPagesTests.post.pub_date,
                         'Тест не прошел, даты нет в контексте'
                         )
        self.assertEqual(post_text_0, PostsPagesTests.post.text,
                         'Тест не прошел, текста нет в контексте'
                         )
        self.assertEqual(post_img_0, PostsPagesTests.post.image,
                         'Тест не прошел, текста нет в контексте'
                         )

    def test_group_posts_on_valid_page(self):
        """Проверяем публикацию с группой на странице группы"""
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test'})
        )
        post_object = response.context['page'][0]
        post_group_0_slug = post_object.group.slug

        self.assertEqual(post_group_0_slug, 'test',
                         'Тест не прошел'
                         )

    def test_group_posts_on_main_page(self):
        """Проверяем публикацию с группой на главной странице"""
        response = self.authorized_client.get(reverse('index'))
        post_object = response.context['page'][0]
        post_group_0_slug = post_object.group.slug

        self.assertEqual(post_group_0_slug, 'test',
                         'Тест не прошел'
                         )

    def test_group_posts_on_invalid_page(self):
        """Проверяем публикацию с невалидной группой на странице группы"""
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test'})
        )
        post_object = response.context['page'][0]
        post_group_0_slug = post_object.group.slug

        self.assertNotEqual(post_group_0_slug, 'wrong_test_group',
                            'Тест не прошел'
                            )

    def test_add_comment_by_user(self):
        """Проверяем публикацию комментария авторизованным пользователем"""
        post = Post.objects.create(
            text='Текст поста',
            group=self.group,
            author=self.user,
        )
        form_fields = {
            'text': 'тестовый комментарий',
            'author': self.user
        }
        self.authorized_client.post(
            reverse('add_comment', kwargs={
                    'username': self.user,
                    'post_id': post.id
            }
            ), data=form_fields, follow=True
        )
        response = self.authorized_client.get(reverse(
            'post', kwargs={'username': self.user, 'post_id': post.id}
        ), data=form_fields, follow=True)

        self.assertContains(response, 'тестовый комментарий')

    def test_add_comment_by_guest(self):
        """Проверяем публикацию комментария неавторизованным пользователем"""
        post = Post.objects.create(
            text='Текст поста',
            group=self.group,
            author=self.user,
        )
        form_fields = {
            'text': 'тестовый комментарий',
            'author': self.user
        }
        self.guest_client.post(
            reverse('add_comment', kwargs={
                'username': self.user,
                'post_id': post.id
            }
            ), data=form_fields, follow=True
        )
        response = self.guest_client.get(reverse(
            'post', kwargs={'username': self.user, 'post_id': post.id}
        ), data=form_fields, follow=True)

        self.assertNotContains(response, 'тестовый комментарий')


class PaginatorViewsTest(TestCase):
    """Проверяем пагинацию с ограничением постов на странице"""
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

        for i in range(13):
            Post.objects.create(
                text=f'Тестовый текст {i}',
                group=cls.group,
                author=cls.user,
            )

    def test_first_page_containse_ten_records(self):
        """Проверяем количество постов на 1ой странице"""
        response = self.client.get(reverse('index'))

        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_containse_three_records(self):
        """Проверяем количество постов на 2ой странице"""
        response = self.client.get(reverse('index') + '?page=2')

        self.assertEqual(len(response.context.get('page').object_list), 3)


class FollowViewsTest(TestCase):
    """Тестирование функционала подписок"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = USER.objects.create_user(username='TestUser')
        cls.user2 = USER.objects.create_user(username='TestUser2')
        cls.user3 = USER.objects.create_user(username='TestUser3')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.authorized_client2 = Client()
        cls.authorized_client2.force_login(cls.user2)
        cls.authorized_client3 = Client()
        cls.authorized_client3.force_login(cls.user3)
        cls.group = Group.objects.create(
            title='Название группы',
            slug='test',
            description='Описание группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=cls.user,
            image='image/gif'
        )

    def test_follow(self):
        """Проверяем подписку"""
        self.authorized_client.get('/TestUser2/follow/')
        response = self.authorized_client.get('/TestUser/')
        self.assertEqual(response.context['follows'], 1)

    def test_unfollow(self):
        """Проверяем отписку"""
        self.authorized_client.get('/TestUser2/unfollow/')
        response = self.authorized_client.get('/TestUser/')
        self.assertEqual(response.context['follows'], 0)

    def test_feed_for_follower(self):
        """Проверяем ленту для подписчика"""
        self.authorized_client.get('/TestUser2/follow/')
        response = self.authorized_client.get('/follow/')
        self.assertContains(response, 'Тестовый текст')

    def test_feed_for_not_follower(self):
        """Проверяем ленту для пользователя"""
        self.authorized_client.get('/TestUser2/follow/')
        self.authorized_client2.get('/TestUser3/follow/')
        form_data = {
            'text': 'Новый пост',
            'group': self.group.id,
        }
        self.authorized_client3.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        response = self.authorized_client.get('/follow/')
        self.assertNotContains(response, 'Новый пост')
