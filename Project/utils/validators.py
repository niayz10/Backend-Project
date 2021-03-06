import os.path

from django.core.exceptions import ValidationError

MAX_FILE_SIZE = 1024000
ALLOWED_EXTENSIONS = ['.jpg', '.png', '.jpeg']
ALLOWED_EXTENSIONS_FOR_BOOK = ['.txt', '.docx']
ALLOWED_EXTENSIONS_FOR_COMICS = ['.pdf', '.jpg', '.jpeg']


def validate_size(value):
    if value.size > MAX_FILE_SIZE:
        raise ValidationError(f'max file size is: {MAX_FILE_SIZE}')


def validate_extension(value):
    split_ext = os.path.splitext(value.name)
    if len(split_ext) > 1:
        ext = split_ext[1]
        if ext.lower() not in ALLOWED_EXTENSIONS:
            raise ValidationError(f'not allowed file, valid extensions: {ALLOWED_EXTENSIONS}')


def validate_extension_for_book(value):
    split_ext = os.path.splitext(value.name)
    if len(split_ext) > 1:
        ext = split_ext[1]
        if ext.lower() not in ALLOWED_EXTENSIONS_FOR_BOOK:
            raise ValidationError(f'not allowed file, valid extensions: {ALLOWED_EXTENSIONS_FOR_BOOK}')


def validate_extension_for_comics(value):
    split_ext = os.path.splitext(value.name)
    if len(split_ext) > 1:
        ext = split_ext[1]
        if ext.lower() not in ALLOWED_EXTENSIONS_FOR_COMICS:
            raise ValidationError(f'not allowed file, valid extensions: {ALLOWED_EXTENSIONS_FOR_COMICS}')
