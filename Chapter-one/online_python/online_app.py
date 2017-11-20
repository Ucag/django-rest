from django.conf import settings
from django.http import HttpResponse, JsonResponse# JsonResponse 用于返回 JSON 数据
from django.conf.urls import url
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import subprocess
setting = {
    'DEBUG':True,
    'ROOT_URLCONF':__name__,
}

settings.configure(**setting)

# 主视图
def home(request):
    with open('index.html','rb') as f:
        html = f.read()
    return HttpResponse(html)
# 执行客户端代码核心函数
def run_code(code):
    try:
        output = subprocess.check_output(['python','-c',code],
                universal_newlines=True,
                stderr=subprocess.STDOUT,
                timeout=30)
    except subprocess.CalledProcessError as e:
        output = e.output
    except subprocess.TimeoutExpired as e:
        output = '\r\n'.join(['Time Out!!!',e.output])
    return output
# API 请求视图
@csrf_exempt
@require_POST
def api(request):
    code = request.POST.get('code')
    output = run_code(code)
    return JsonResponse(data={'output':output})
# URL 配置
urlpatterns = [url('^$',home,name='home'),
               url('^api/$',api,name='api')]

if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)