# Generated by Django 4.2.7 on 2023-11-19 14:16

import app.base.services
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('1', 'Обычный'), ('2', 'Устный')], default='1', max_length=7)),
                ('description', models.TextField(default='')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категорий',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'квиз',
                'verbose_name_plural': 'квизы',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveIntegerField()),
                ('text', models.TextField(blank=True, max_length=1000, null=True)),
                ('audio', models.FileField(blank=True, null=True, upload_to=app.base.services.get_audio_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3'])])),
                ('image', models.ImageField(blank=True, null=True, upload_to=app.base.services.get_image_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])])),
                ('video', models.FileField(blank=True, null=True, upload_to=app.base.services.get_video_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])])),
                ('correct_text_answer', models.CharField(blank=True, default='Правильный ответ', max_length=100, null=True)),
                ('order_num', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('detailed_answer', models.CharField(blank=True, max_length=1000, null=True)),
                ('detailed_answer_img', models.ImageField(blank=True, null=True, upload_to=app.base.services.get_image_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='main.category')),
            ],
            options={
                'verbose_name': 'вопрос',
                'verbose_name_plural': 'вопросы',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='main.question')),
            ],
            options={
                'verbose_name': 'вариант ответа',
                'verbose_name_plural': 'варианты ответа',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='main.quiz'),
        ),
        migrations.AddIndex(
            model_name='quiz',
            index=models.Index(fields=['author'], name='main_quiz_author__d56128_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['category'], name='main_questi_categor_3d910d_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['order_num'], name='main_questi_order_n_4d8efa_idx'),
        ),
        migrations.AddIndex(
            model_name='option',
            index=models.Index(fields=['question'], name='main_option_questio_8860eb_idx'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['quiz'], name='main_catego_quiz_id_0b015c_idx'),
        ),
    ]
