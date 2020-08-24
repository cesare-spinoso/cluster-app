import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-manually-generate-key'

    HERE = os.path.dirname(os.path.realpath(__file__))

    UPLOAD_FOLDER = HERE + '/app/static/data/'
    ALLOWED_FILE_EXTENSIONS = ['CSV']

    IMAGE_FOLDER = HERE + '/app/static/images/'

