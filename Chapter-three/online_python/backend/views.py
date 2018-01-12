import subprocess
from django.http import HttpResponse
from django.db import models
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CodeListSerializer, CodeSerializer
from .models import Code
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    去除 CSRF 检查
    """

    def enforce_csrf(self, request):
        return


class APIRunCodeMixin(object):
    """
    运行代码操作
    """

    def run_code(self, code):
        """
        运行所给的代码，并返回执行结果
        :params code: str, 需要被运行的代码
        :return: str, 运行结果
        """
        try:
            output = subprocess.check_output(['python', '-c', code],  # 运行代码
                                             stderr=subprocess.STDOUT,  # 重定向错误输出流到子进程
                                             universal_newlines=True,  # 将返回执行结果转换为字符串
                                             timeout=30)  # 设定执行超时时间
        except subprocess.CalledProcessError as e:  # 捕捉执行失败异常
            output = e.output  # 获取子进程报错信息
        except subprocess.TimeoutExpired as e:  # 捕捉超时异常
            output = '\r\n'.join(['Time Out!', e.output])  # 获取子进程报错，并添加运行超时提示
        return output  # 返回执行结果


class CodeViewSet(APIRunCodeMixin, ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def list(self, request, *args, **kwargs):
        """
        使用专门的列表序列化器，而非默认的序列化器
        """
        serializer = CodeListSerializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def run_create_or_update(self, request, serializer):
        """
        create 和 update 的共有逻辑，仅仅是简单的多了 run 参数的判断
        """
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            serializer.save()
            if 'run' in request.query_params.keys():
                output = self.run_code(code)
                data = serializer.data
                data.update({'output': output})
                return Response(data=data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        return self.run_create_or_update(request, serializer)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        return self.run_create_or_update(request, serializer)


class RunCodeAPIView(APIRunCodeMixin, APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        output = self.run_code(request.data.get('code'))
        return Response(data={'output': output}, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        try:
            code = Code.objects.get(pk=request.query_params.get('id'))
        except models.ObjectDoesNotExist:
            return Response(data={'error': 'Object Not Found'}, status=status.HTTP_404_NOT_FOUND)
        output = self.run_code(code.code)
        return Response(data={'output': output}, status=status.HTTP_200_OK)


def home(request):
    with open('frontend/index.html', 'rb') as f:
        content = f.read()
    return HttpResponse(content)


def js(request, filename):
    with open('frontend/{}'.format(filename), 'rb') as f:
        js_content = f.read()
    return HttpResponse(content=js_content,
                        content_type='application/javascript')  # 返回 js 响应


def css(request, filename):
    with open('frontend/{}'.format(filename), 'rb') as f:
        css_content = f.read()
    return HttpResponse(content=css_content,
                        content_type='text/css')
