def get_audio_path(instance, filename):
    return f'audio/game/{instance.category.quiz.author.profile.nickname}/' \
           f'{instance.category.quiz.title}/{instance.category.name}/' \
           f'{filename}'


def get_image_path(instance, filename):
    return f'images/game/{instance.category.quiz.author.profile.nickname}/' \
           f'{instance.category.quiz.title}/{instance.category.name}/' \
           f'{filename}'


def get_video_path(instance, filename):
    return f'videos/game/{instance.category.quiz.author.profile.nickname}/' \
           f'{instance.category.quiz.title}/{instance.category.name}/' \
           f'{filename}'