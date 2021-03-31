from django.test import TestCase
from posts.models import Post, Group, USER


class PostsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Название',
            slug='Ссылка',
            description='Описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=USER.objects.create(username='TestUser'),
        )

    def test_verbose_name(self):
        """Проверка verbose_name"""

        post = self.post
        field_verboses = {
            'text': 'Текст публикации',
            'group': 'Сообщество',
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected
                )

    def test_help_text(self):
        """Проверка help_text"""

        post = self.post
        field_help_texts = {
            'group': 'Укажите сообщество',
            'text': 'Напишите что-нибудь'
        }

        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected
                )

    def test_str(self):
        """Проверка __str__"""

        post = PostsModelTest.post
        text = post.text
        self.assertEqual(str(post), text[:15])

    def test_group_title(self):
        """Проверка group_title"""

        group = PostsModelTest.group
        title = str(group)
        self.assertEqual(title, group.title)
