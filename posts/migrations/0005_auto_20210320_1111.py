# Generated by Django 2.2 on 2021-03-20 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20210222_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, help_text='Укажите группу', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='posts.Group', verbose_name='Сообщество'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(help_text='Напишите что-нибудь', verbose_name='Текст публикации'),
        ),
    ]
