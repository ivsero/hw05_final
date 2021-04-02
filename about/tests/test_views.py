from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import USER

USER = get_user_model()


class StaticViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = USER.objects.create_user(username='TestUser')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_pages_accessible_by_name(self):
        """URL, генерируемые при помощи имен доступны"""
        name_list = (
            'about:author',
            'about:tech',
        )

        for name in name_list:
            with self.subTest(name):
                response = self.guest_client.get(reverse(name))
                self.assertEqual(
                    response.status_code,
                    200,
                    'Что-то пошло не так. Проверьте файл urls.py'
                )

    def test_about_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'about/author.html': reverse('about:author'),
            'about/tech.html': reverse('about:tech'),
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(
                    response,
                    template,
                    'Что-то пошло не так. Проверьте файл urls.py'
                )
