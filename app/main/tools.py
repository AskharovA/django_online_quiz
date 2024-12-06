from PIL import Image
from .models import Quiz


def resize_player_avatar(instance):
    img = Image.open(instance.image.path)
    if img.height > 250 or img.width > 250:
        size = 250, 250
        img.thumbnail(size, Image.LANCZOS)
        img.save(instance.image.path)


def check_quiz_for_errors(quiz: Quiz):
    errors_message = []
    errors = 0
    for category in quiz.categories.all():
        questions = category.questions.all()
        if questions.exists():
            for question in questions:
                if category.type == '1':
                    options = question.options.all()
                    if options.exists():
                        if options.filter(is_correct=True).count() > 1:
                            errors_message += [(f'В категории {category.name} имеется вопрос '
                                               f'с более 1 вариантом ответа.')]
                            errors += 1
                        elif options.filter(is_correct=True).count() == 0:
                            errors_message += [(f'В категории {category.name} имеется вопрос '
                                               f'без правильного варианта ответа.')]
                            errors += 1
                    else:
                        errors_message += [f'В категории {category.name} имеется вопрос без варианов ответа.']
                        errors += 1
        else:
            errors_message += [f'Категория {category.name} пуста.']
            errors += 1
    if not errors_message:
        errors_message = ['Ошибок нет.']
    return {
        'errors': errors,
        'message': errors_message,
    }


def load_avatars():
    """ Load Default Avatars Script """
    from app.game.models import PlayerAvatar
    from pathlib import Path
    from django.conf import settings
    from django.core.files.base import ContentFile

    avatars_dir_path = Path(settings.MEDIA_ROOT) / "images" / "game" / "avatars"

    for image_file in Path(avatars_dir_path).iterdir():
        print(image_file.name)
        if image_file.is_file():
            print("Выполнено")
            with open(image_file, 'rb') as f:
                PlayerAvatar.objects.create(image=ContentFile(f.read(), name=image_file.name))
