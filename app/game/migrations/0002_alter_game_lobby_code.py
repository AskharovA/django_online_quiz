# Generated by Django 4.2.7 on 2023-11-23 09:53

import app.game.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='lobby_code',
            field=models.CharField(default=app.game.models.generate_code_for_game, max_length=29),
        ),
    ]
