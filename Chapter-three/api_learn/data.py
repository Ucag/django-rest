from django import setup
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','api_learn.settings')
setup()

from rest_learn.models import TestModel

data_set = {
    'ls':"""import os\r\nprint(os.listdir())""",
    'pwd':"""import os\r\nprint(os.getcwd())""",
    'hello world':"""print('Hello world')"""
}
for name, code in data_set.items():
    TestModel.objects.create(name=name,code=code)

print('Done')