# Generated by Django 4.2.7 on 2024-02-02 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameboard_app', '0004_remove_question_file_alter_question_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pic',
            field=models.ImageField(blank=True, default='', null=True, upload_to='question_images/'),
        ),
    ]
