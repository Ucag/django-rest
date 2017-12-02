from django.views import View  # 引入最基本的类视图
from django.http import JsonResponse, HttpResponse  # 引入现成的响应类
from django.core.serializers import serialize  # 引入序列化函数
from .models import CodeModel  # 引入 Code 模型，记得加个 `.`  哦。
import json  # 引入 json 库，我们会用它来处理 json 字符串。
from .mixins import APIDetailMixin, APIUpdateMixin, \
    APIDeleteMixin, APIListMixin, APIRunCodeMixin, \
    APICreateMixin, APIMethodMapMixin, APISingleObjectMixin  # 引入我们编写的所有 Mixin


# 定义最基本的 API 视图
class APIView(View):
    def response(self,
                 queryset=None,
                 fields=None,
                 **kwargs):
        """
        序列化传入的 queryset 或 其他 python 数据类型。返回一个 JsonResponse 。
        :param queryset: 查询集，可以为 None
        :param fields: 查询集中需要序列化的字段，可以为 None
        :param kwargs: 其他需要序列化的关键字参数
        :return: 返回 JsonResponse
        """

        # 根据传入参数序列化查询集，得到序列化之后的 json 字符串
        if queryset and fields:
            serialized_data = serialize(format='json',
                                        queryset=queryset,
                                        fields=fields)
        elif queryset:
            serialized_data = serialize(format='json',
                                        queryset=queryset)
        else:
            serialized_data = None
        # 这一步很重要，在经过上面的查询步骤之后， serialized_data 已经是一个字符串
        # 我们最终需要把它放入 JsonResponse 中，JsonResponse 只接受 python 数据类型
        # 所以我们需要先把得到的 json 字符串转化为 python 数据结构。
        instances = json.loads(serialized_data) if serialized_data else 'No instance'
        data = {'instances': instances}
        data.update(kwargs)  # 添加其他的字段
        return JsonResponse(data=data)  # 返回响应


#
class APICodeView(APIListMixin,  # 获取列表
                  APIDetailMixin,  # 获取当前请求实例详细信息
                  APIUpdateMixin,  # 更新当前请求实例
                  APIDeleteMixin,  # 删除当前实例
                  APICreateMixin,  # 创建新的的实例
                  APIMethodMapMixin,  # 请求方法与资源操作方法映射
                  APIView):  # 记得在最后继承 APIView
    model = CodeModel  # 传入模型

    def list(self):  # 这里仅仅是简单的给父类的 list 函数传参。
        return super(APICodeView, self).list(fields=['name'])


class APIRunCodeView(APIRunCodeMixin,
                     APISingleObjectMixin,
                     APIView):
    model = CodeModel  # 传入模型

    def get(self, request, *args, **kwargs):
        """
        GET 请求仅对能获取到 pk 值的 url 响应
        :param request: 请求对象
        :param args: 位置参数
        :param kwargs: 关键字参数
        :return: JsonResponse
        """
        instance = self.get_object()  # 获取对象
        code = instance.code  # 获取代码
        output = self.run_code(code)  # 运行代码
        return self.response(output=output, status='Successfully Run')  # 返回响应

    def post(self, request, *args, **kwargs):
        """
        POST 请求可以被任意访问，并会检查 url 参数中的 save 值，如果 save 为 true 则会
        保存上传代码。
        :param request: 请求对象
        :param args: 位置参数
        :param kwargs: 关键字参数
        :return: JsonResponse
        """
        code = self.request.POST.get('code')  # 获取代码
        save = self.request.GET.get('save') == 'true'  # 获取 save 参数值
        name = self.request.POST.get('name')  # 获取代码片段名称
        output = self.run_code(code)  # 运行代码
        if save:  # 判断是否保存代码
            instance = self.model.objects.create(name=name, code=code)
        return self.response(status='Successfully Run and Save',
                             output=output)  # 返回响应

    def put(self, request, *args, **kwrags):
        """
        PUT 请求仅对更改操作作出响应
        :param request: 请求对象
        :param args: 位置参数
        :param kwrags: 关键字参数
        :return: JsonResponse
        """
        code = self.request.PUT.get('code')  # 获取代码
        name = self.request.PUT.get('name')  # 获取代码片段名称
        save = self.request.GET.get('save') == 'true'  # 获取 save 参数值
        output = self.run_code(code)  # 运行代码
        if save:  # 判断是否需要更改代码
            instance = self.get_object()  # 获取当前实例
            setattr(instance, 'name', name)  # 更改名字
            setattr(instance, 'code', code)  # 更改代码
            instance.save()
        return self.response(status='Successfully Run and Change',
                             output=output)  # 返回响应


# 主页视图
def home(request):
    """
    读取 'index.html' 并返回响应
    :param request: 请求对象
    :return: HttpResponse
    """
    with open('frontend/index.html', 'rb') as f:
        content = f.read()
    return HttpResponse(content)


# 读取 js 视图
def js(request, filename):
    """
    读取 js 文件并返回 js 文件响应
    :param request: 请求对象
    :param filename: str-> 文件名
    :return: HttpResponse
    """
    with open('frontend/js/{}'.format(filename), 'rb') as f:
        js_content = f.read()
    return HttpResponse(content=js_content,
                        content_type='application/javascript')  # 返回 js 响应


# 读取 css 视图
def css(request, filename):
    """
    读取 css 文件，并返回 css 文件响应
    :param request: 请求对象
    :param filename: str-> 文件名
    :return: HttpResponse
    """
    with open('frontend/css/{}'.format(filename), 'rb') as f:
        css_content = f.read()
    return HttpResponse(content=css_content,
                        content_type='text/css')  # 返回 css 响应
