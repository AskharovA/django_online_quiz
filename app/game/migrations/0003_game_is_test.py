# Generated by Django 4.2.7 on 2024-12-05 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_game_lobby_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_test',
            field=models.BooleanField(default=False),
        ),
    ]
