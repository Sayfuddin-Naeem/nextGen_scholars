import os

def get_upload_to(instance, filename):
    return os.path.join('course/images/', filename)

