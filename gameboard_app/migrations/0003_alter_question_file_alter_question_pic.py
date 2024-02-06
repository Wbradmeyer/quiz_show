# Generated by Django 4.2.7 on 2024-01-30 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameboard_app', '0002_category_game_assigned_game_creator_game_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='file',
            field=models.FileField(blank=True, default='', null=True, upload_to='question_files/'),
        ),
        migrations.AlterField(
            model_name='question',
            name='pic',
            field=models.ImageField(blank=True, default='', null=True, upload_to='question_images/'),
        ),
    ]