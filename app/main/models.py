from django.db import models
from app.users.models import User
from django.core.validators import FileExtensionValidator
from app.base.services import get_image_path, get_audio_path, get_video_path
import os


class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    for_test = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'квиз'
        verbose_name_plural = 'квизы'
        indexes = [
            models.Index(fields=['author']),
        ]


class Category(models.Model):
    class Type(models.TextChoices):
        DEFAULT = '1', 'Обычный'
        TEXT = '2', 'Устный'
    quiz = models.ForeignKey(Quiz, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=7, choices=Type.choices, default=Type.DEFAULT)
    description = models.TextField(default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категорий'
        indexes = [
            models.Index(fields=['quiz']),
        ]


class Question(models.Model):
    category = models.ForeignKey(Category, related_name='questions', on_delete=models.CASCADE)
    points = models.PositiveIntegerField()
    text = models.TextField(max_length=1000, blank=True, null=True)
    audio = models.FileField(
        upload_to=get_audio_path,
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])],
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to=get_image_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])],
        blank=True,
        null=True,
    )
    video = models.FileField(
        upload_to=get_video_path,
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        blank=True,
        null=True,
    )
    correct_text_answer = models.CharField(max_length=100, default='Правильный ответ', blank=True, null=True)
    order_num = models.PositiveSmallIntegerField(null=True, blank=True)
    detailed_answer = models.CharField(max_length=1000, blank=True, null=True)
    detailed_answer_img = models.ImageField(
        blank=True,
        null=True,
        upload_to=get_image_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])]
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['order_num']),
        ]
        ordering = ['points']

    def get_correct_option(self):
        return self.options.filter(is_correct=True).first().text

    def delete(self, using=None, keep_parents=False):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        if self.audio:
            if os.path.isfile(self.audio.path):
                os.remove(self.audio.path)
        if self.video:
            if os.path.isfile(self.video.path):
                os.remove(self.video.path)
        super(Question, self).delete()


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'вариант ответа'
        verbose_name_plural = 'варианты ответа'
        indexes = [
            models.Index(fields=['question']),
        ]
