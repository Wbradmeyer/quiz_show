# Generated by Django 4.2.7 on 2024-02-02 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameboard_app', '0003_alter_question_file_alter_question_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='file',
        ),
        migrations.AlterField(
            model_name='question',
            name='pic',
            field=models.ImageField(blank=True, default='', height_field='200px', null=True, upload_to='question_images/', width_field='200px'),
        ),
    ]
