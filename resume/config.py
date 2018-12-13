import os

basedir = os.path.abspath(os.path.dirname(__file__))
    




DEBUG = False
TESTING = False
CSRF_ENABLED = True
SECRET_KEY = 'this-really-needs-to-be-changed'


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "postgresql://erick:rooster1@localhost/resumecore"
UPLOAD_FOLDER = '/home/erick/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'xlsx'])

