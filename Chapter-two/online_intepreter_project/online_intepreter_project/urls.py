# 这是我们的 URL 入口配置，我们直接将入口配置到具体的 URL 上。

from django.conf.urls import url, include  # 引入需要用到的配置函数
# include 用来引入其他的 URL 配置。参数可以是个路径字符串，也可以是个 url 对象列表

from online_intepreter_app.views import APICodeView, APIRunCodeView, home, js, css  # 引入我们的视图函数
from django.views.decorators.csrf import csrf_exempt  # 同样的，我们不需要使用 csrf 功能。

# 注意我们这里的 csrf_exempt 的用法，这和将它作为装饰器使用的效果是一样的

# 普通的集合操作 API
generic_code_view = csrf_exempt(APICodeView.as_view(method_map={'get': 'list',
                                                                'post': 'create'}))  # 传入自定义的 method_map 参数
# 针对某个对象的操作 API
detail_code_view = csrf_exempt(APICodeView.as_view(method_map={'get': 'detail',
                                                               'put': 'update',
                                                               'delete': 'remove'}))
# 运行代码操作 API
run_code_view = csrf_exempt(APIRunCodeView.as_view())
# Code 应用 API 配置
code_api = [
    url(r'^$', generic_code_view, name='generic_code'),  # 集合操作
    url(r'^(?P<pk>\d*)/$', detail_code_view, name='detail_code'),  # 访问某个特定对象
    url(r'^run/$', run_code_view, name='run_code'),  # 运行代码
    url(r'^run/(?P<pk>\d*)/$', run_code_view, name='run_specific_code')  # 运行特定代码
]
api_v1 = [url('^codes/', include(code_api))]  # API 的 v1 版本
api_versions = [url(r'^v1/', include(api_v1))]  # API 的版本控制入口 URL
urlpatterns = [
    url(r'^api/', include(api_versions)),  # API 访问 URL
    url(r'^$', home, name='index'),  # 主页视图
    url(r'^js/(?P<filename>.*\.js)$', js, name='js'),  # 访问 js 文件，记得，最后没有 /
    url(r'^css/(?P<filename>.*\.css)$', css, name='css')  # 访问 css 文件，记得，最后没有 /
]
