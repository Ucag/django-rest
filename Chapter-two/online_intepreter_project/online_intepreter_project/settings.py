# 这是我们的配置文件。在配在黑文件中，删除了其他我们用不上的配置项。

import os

# BASE_DIR最终的值为 `manage.py` 所在路径。这是因为 `manage.py` 时我们整个项目的入口，
# 所以整个项目也是在 `manage.py` 所在路径下运行的，在写代码时，也应该考虑到跟路径是 manage.py
# 所在路径。比如，当我们从  `views.py` 引入 `models` 模块时，写的是 `from .models import ..`，
# 如果仅仅是 `from models import ...` 就可能会出错，因为这句话的意思是从当前路径下引入这个模块，
# 但我们的项目是在 `manange.py` 运行的路径下执行的，这个路径下更本不会有 `models.py` 这个文件，所以
# 我们要加上 `.` 路径符，表示是在本模块所在的路径下的模块文件。所以大家平时写代码也应该养成加上 `.` 路径符
# 的习惯。
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '=@_j0i9=3-93xb1_9cr)i!ra56o1f$t&jhfb&pj(2n+k9ul8!l'

DEBUG = True
# INSTALLED_APPS 项用来告诉 django 我们需要加载哪些 APP 的配置，同时，在我们运行
# # `python manage.py makemigrations` 或者 `python manage.py migrate` 时，django
# 会搜索其中应用的模型文件，并建立相应的模型。这次我们用到了模型，所以需要用到这个配置项。
INSTALLED_APPS = ['online_intepreter_app']
# 由于 django 对 PUT 方法没有很好的支持，所以我们自己写了个简单的中间件，来处理我们的 PUT 请求。
MIDDLEWARE = ['online_intepreter_app.middlewares.put_middleware']
# 根 URL 配置，这也是 django URL 的入口，所有的请求将会通过这个 URL 配置来访问我们应用的相应部分
ROOT_URLCONF = 'online_intepreter_project.urls'
# 这是我们的数据库配置，用来配置我们的应用。
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
