# Generated by Django 2.2 on 2021-03-21 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20210320_1111'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Сообщество', 'verbose_name_plural': 'Сообщества'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Публикация', 'verbose_name_plural': 'Публикации'},
        ),
    ]
