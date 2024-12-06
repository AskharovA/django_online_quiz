# from celery import shared_task
# from PIL import Image
# from io import BytesIO
# from django.core.files.base import ContentFile
#
#
# @shared_task
# def resize_image(instance_id):
#     from .models import Question
#
#     instance = Question.objects.get(id=instance_id)
#     image = Image.open(instance.image)
#
#     image = image.resize(calculate_image_size(image.width, image.height), Image.Resampling.LANCZOS)
#
#     buffer = BytesIO()
#     image.save(buffer, format='JPEG')
#     buffer.seek(0)
#
#     instance.image.save(f'{instance.image.name}', ContentFile(buffer.read()), save=False)
#     buffer.close()
#
#     instance.save()
#
#
# def calculate_image_size(width, height, max_size=(600, 400)):
#     ratio = min(max_size[0] / width, max_size[1] / height)
#     return int(width * ratio), int(height * ratio)
