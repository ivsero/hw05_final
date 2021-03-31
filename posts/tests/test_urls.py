from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post, Group, USER

USER = get_user_model()


class PostsURLTests(TestCase):
    """Тестирование URL"""
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

    def test_urls_exists_for_guests(self):
        """URL доступны для всех пользователей"""
        urls_list = (
            '/',
            '/group/test/',
            '/TestUser/',
            '/TestUser/1/',
        )

        for path in urls_list:
            with self.subTest(path):
                response = self.guest_client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_urls_exists_for_authorized_users(self):
        """URL доступны для авторизированных пользователей"""
        urls_list = (
            '/',
            '/group/test/',
            '/TestUser/1/edit/',
        )

        for path in urls_list:
            with self.subTest(path):
                response = self.authorized_client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_urls_redirect_anonymous(self):
        """URL редиректят гостей"""
        urls_list = (
            '/TestUser/1/edit/',
            '/new/',
        )

        for path in urls_list:
            with self.subTest(path):
                response = self.guest_client.get(path)
                self.assertEqual(response.status_code, 302)

    def test_404_response(self):
        """Проверка ответа 404"""
        response = self.guest_client.get('404/')
        self.assertEqual(response.status_code, 404)

    def test_post_edit_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу /post_edit/ перенаправит анонимного
        пользователя на страницу поста.
        """
        response = PostsURLTests.guest_client.get(
            '/TestUser/1/edit/', follow=True)
        self.assertRedirects(
            response, '/TestUser/1/')

    def test_new_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу /new/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = PostsURLTests.guest_client.get('/new/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/new/')

    def test_urls_uses_correct_templates(self):
        """URL используют корректный шаблон"""
        templates_url_names = {
            'index.html': '/',
            'group.html': '/group/test/',
            'post_form.html': '/new/',
        }

        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
