from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import USER

USER = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = USER.objects.create_user(username='TestUser')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_urls_uses_correct_templates(self):
        """URL доступны для всех пользователей"""
        urls_list = (
            '/about/author/',
            '/about/tech/',
        )

        for path in urls_list:
            with self.subTest(path):
                response = self.guest_client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_templates(self):
        """URL используют корректный шаблон"""
        templates_url_names = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/',
        }

        for template, reverse_name in templates_url_names.items():
            with self.subTest(reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
