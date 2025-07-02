from django.core.exceptions import ValidationError
import os


def validate_video_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Faqat video formatdagi fayllarga ruxsat beriladi: .mp4, .mov, .avi, .mkv')
