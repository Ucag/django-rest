from django.conf import settings
from django.http import HttpResponse
from django.conf.urls import url
from django import setup
setting = {
    'DEBUG':True,
    'ROOT_URLCONF':__name__
}

settings.configure(**setting)

def home(request):
    return HttpResponse('Hello world!')

urlpatterns = [url('^$',home,name='home')]

if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)