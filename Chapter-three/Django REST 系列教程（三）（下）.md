#Django REST 系列教程（三）（下）
终于考完试了。今天有空把这部分完成了，大家久等了。


---
##设计
交互还是和以前一样，只是 API 略微有些变动。如果需要 创建时就运行一次代码 ，我们只需要在对应操作之后加上 `run` 参数就可以了。 比如 向 `/code/?run` post  就可以创建并运行代码了，更新并运行也是同理。

如果需要单独运行代码 向 `/run/` post 代码解可以了，如果需要运行特定的实例，只需使用 get 请求在后面加上 `id` 参数就行。比如 GET  `/run/?id=1` 就会得到代码实例 id 为 1 的运行结果。 

##准备工作。
创建一个新的项目 `online_python` 

```
django-admin startproject online_python
```

然后在 `online_python` 项目内创建一个 APP 

```
python manage.py startapp backend
```

然后创建如下的目录结构

```
online_python/
    frontend/
        index.js # 空文件
        index.html # 空文件
        vue.js # vue 的源文件
        bootstrap.js # bootstrap 的 js文件
        jquery.js # bootstrap.js 的依赖
        bootstrap.css # bootstrap 核心 css 文件
    backend/
        ... # APP 相关
    manage.py
```


编写配置，把我们的 APP 和 DRF 添加进去。

`settings.py`
```python
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'backend'
]
...
```

准备完毕。

##后端开发
我们还是先从后端写起。

创建模型：

`models.poy`
```python

from django.db import models

class Code(models.Model):
    name = models.CharField(max_length=20, blank=True)
    code = models.TextField()
    
```


在模型创建完成之后，我们需要创建首次迁移。

回到项目根目录，创建并运行迁移，同时把管理员账户创建好。

```
python manage.py makemigrations
python manage.py migrate

python manage.py craetesuperuser
```


创建序列化器：

在 `backend` 下新建文件 `serializers.py`：

`serializers.py`
```python
from rest_framework import serializers
from .models import Code

#创建序列化器
class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__' #序列化全部字段

#用于列表展示的序列化器
class CodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ('id', 'name')
```

为什么会有两个序列化器？

因为我们请求  `list` 时，我们只需要 `Code` 实例的 `name` 和 `id` 字段，在其它的情况下又需要用到全部的字段。所以我们需要两个序列化器。

现在就可以开始编写视图了。

在顶部引入我们需要的包。

`views.py`
```python
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
```

`subprocess` 用于运行客户端代码的包。

`HttpResponse` 用于静态文件服务视图。

`models` 主要是为了使用它的 `ObjectDoseNotExist` 异常。

`APIView` 最基本的 DRF API 视图。

`Response` DRF 响应对象。

`status` DRF 为我们封装好的状态响应码。

`CodeSerializer`、`CodeListSerializer` 需要用到的序列化器。

`Code` Code 模型。

`SessionAuthentication` 用于编写禁止 CSRF 的认证后端。我们会在下面详细的说明。

我们先把运行代码的 Mixin 给复制粘贴过来。

`views.py`
```python
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

```

创建 CodeViewSet 

`views.py`
```python
class CodeViewSet(APIRunCodeMixin, ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer
```


这是最最基本的 CodeViewSet 。 DRF 的 ViewSet 为我们默认编写好了各个请求方法对应的操作映射。不带参数的 `get` 请求对应 `list` 操作，`post` 请求对应 `create` 操作等等。这也是它叫做 `ViewSet` (视图集)的原因，它帮我们完成了基本的几个视图原型。`ModelViewSet` 让我们可以直接把视图和模型相关联起来，比如 `list` 会直接返回模型序列化之后的结果，而不需要我们手动编写这些动作。

`list` 默认使用的是 `serializer_class` 指定的序列化器，但是由于我们需要在 `list` 动作的时候用另一个序列化器，所以我们需要简单的重写这个动作。


`views.py`
```python
    def list(self, request, *args, **kwargs):
        """
        使用专门的列表序列化器，而非默认的序列化器
        """
        serializer = CodeListSerializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)
```


`create` 操作需要判断是否有 `run` 参数，所以我们也需要重写 `create` 操作。

`views.py`
```python
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

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
```

我们知道 Django 会向视图函数默认传入一个 `Request` 对象，但是这里的 `Request` 对象是 DRF 的请求对象。 

`request.query_params` 是 DRF 请求对象获取请求参数的方式，`query_params` 保存了所有的请求参数。

在 Django 的表单中，我们可以使用 `form.save()` 来直接把数据保存到模型中。在序列化器中也是同理，我们可以使用 `serializer.save()` 把序列化器中的数据直接保存到模型中。

同样的，我们的 `update` 操作也需要做同样的事情。

`views.py`
```python
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)

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
```

`get_object` 是用于提取当前请求对应的实例方法。

我们发现，`create` 和 `update` 除了在创建序列化器实例不同之外，我们完全可以把他们的逻辑放在一起。

`views.py`
```python
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

```

到这里我们主要的 API 就完成了。

现在需要完成可以直接运行代码的 API 。

`views.py`
```python
class RunCodeAPIView(APIRunCodeMixin, APIView):

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

```


接下来完成静态文件服务的请求视图，把之前写的代码复制粘贴过来，稍稍做一些更改。

`views.py`
```python
def home(request):
    with open('frontend/index.html', 'rb') as f:
        content = f.read()
    return HttpResponse(content)


def js(request, filename):
    with open('frontend/{}'.format(filename), 'rb') as f:
        js_content = f.read()
    return HttpResponse(content=js_content,
                        content_type='application/javascript') 


def css(request, filename):
    with open('frontend/{}'.format(filename), 'rb') as f:
        css_content = f.read()
    return HttpResponse(content=css_content,
                        content_type='text/css')

```


完成我们的 url 配置。

`urls.py`
```python
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from backend.views import CodeViewSet, RunCodeAPIView, home, js, css

router = DefaultRouter()
router.register(prefix='code', viewset=CodeViewSet, base_name='code')

API_V1 = [url(r'^run/$', RunCodeAPIView.as_view(), name='run')]

API_V1.extend(router.urls)

API_VERSIONS = [url(r'^v1/', include(API_V1))]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(API_VERSIONS)),
    url(r'^js/(?P<filename>.*\.js)$', js, name='js'),
    url(r'^css/(?P<filename>.*\.css)$', css, name='css'),
    url(r'^$', home, name='home')
]
```

在之前，我们对于 csrf 的处理都是使用的 `csrf_exempt` ，现在我们的 API 都是使用 Router 来生成了。该怎么办呢？

在 Django 中，一个请求在到达视图之前，会先经过中间件的处理。在 DRF 中，所有的请求会先经过认证处理，如果请求认证通过，则会让请求访问视图，如果认证不通过，请求就无法到达视图。所以，我们采用的方法是重写认证。

在 APIView 中，如果提供了 `authentication_classes` ，则会使用提供的认证后端来进行认证。如果没有提供，则会使用默认的认证后端。有关的细节我们将会在之后的章节中讨论，大家就先了解到这里。提供 csrf 验证的是一个叫做 `SessionAuthentication` 的认证后端，我们需要重新改写其中验证 csrf 的方法。

`views.py`
```python
class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    去除 CSRF 检查
    """

    def enforce_csrf(self, request):
        return
```

这样就完成了。


然后把它放进我们视图中。

整个 `views.py` 的代码就是这样的。

`views.py`
```python
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
                        content_type='application/javascript')  


def css(request, filename):
    with open('frontend/{}'.format(filename), 'rb') as f:
        css_content = f.read()
    return HttpResponse(content=css_content,
                        content_type='text/css')

```


DRF 还为我们提供了可视化的 API 。运行开发服务器，直接访问 `http://127.0.0.1:8000/api/v1/`

你会看到这样的页面

![API 根路径](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-three/imgs/API%20ROOT.png)

DRF 为我们列出了 `code` API ，点击连接地址，我们就可以在跳转的页面中直接进行相关的操作。比如用 POST 创建一个新的代码实例。

![post 示例](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-three/imgs/post%20%E7%A4%BA%E4%BE%8B.png)
提交之后，我们来到了这样的页面。
![提交结果](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-three/imgs/%E6%8F%90%E4%BA%A4%E7%BB%93%E6%9E%9C.png)

然后我们直接在浏览器中访问这个实例的地址，在这里，我的 id 是 46 ，你们根据自己的实例创建 id 来访问。

![实例详情](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-three/imgs/%E5%AE%9E%E4%BE%8B%E8%AF%A6%E6%83%85.png)

这个可视化 API 有什么用呢？最大的用处莫过于在前端开发的时候，看看不同的接口会返回什么样的数据类型，具体的格式是什么，这样前端才好对相应的数据做正确的处理。当前端在开发时对接口有什么疑问，可以自行用它来做实验。方便了前后端的接口协作处理。

##前端开发
首先在入口 html 页面中写好组件入口。

`index.html`
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>在线 Python 解释器</title>
    <link rel="stylesheet" type="text/css" href="css/bootstrap.css">
</head>
<body>
<div id="app"></div>
<script src="js/jquery.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/vue.js"></script>
<script src="js/index.js"></script>
</body>
</html>
```

接下来的工作都将会在 `index.js` 中完成。

先编写好 API ：
`index.js`
```javascript
let api = {
    v1: {
        run: function () {
            return '/api/v1/run/'
        },
        code: {
            list: function () {
                return '/api/v1/code/'
            },
            create: function (run = false) {
                let base = '/api/v1/code/';
                return run ? base + '?run' : base
            },
            detail: function (id, run = false) {
                let base = `/api/v1/code/${id}/`;
                return run ? base + '?run' : base
            },
            remove: function (id) {
                return api.v1.code.detail(id, false)
            },
            update: function (id, run = false) {
                return api.v1.code.detail(id, run)
            }
        }
    }
}
```

我们还需要 Store 来管理状态。我们知道 Store 是管理和储存公共数据的地方，同时我们对于 API 的操作其实就是对于数据的操作，我们应该把所有直接和 API 相关的请求和操作都定义在这里。

`index.js`
```javascript
let store = {
    state: {
        list: [],
        code: '',
        name: '',
        id: '',
        output: ''
    },
    actions: {
        run: function (code) { //运行代码
            $.post({
                url: api.v1.run(),
                data: {code: code},
                dataType: 'json',
                success: function (data) {
                    store.state.output = data.output
                }
            })
        },
        runDetail: function (id) { //运行特定的代码
            $.getJSON({
                url: api.v1.run() + `?id=${id}`,
                success: function (data) {
                    store.state.output = data.output
                }
            })
        },
        freshList: function () { //获得代码列表
            $.getJSON({
                url: api.v1.code.list(),
                success: function (data) {
                    store.state.list = data
                }
            })
        },
        getDetail: function (id) {//获得特定的代码实例
            $.getJSON({
                url: api.v1.code.detail(id),
                success: function (data) {
                    store.state.id = data.id;
                    store.state.name = data.name;
                    store.state.code = data.code;
                    store.state.output = '';
                }
            })
        },
        create: function (run = false) { //创建新代码
            $.post({
                url: api.v1.code.create(run),
                data: {
                    name: store.state.name,
                    code: store.state.code
                },
                dataType: 'json',
                success: function (data) {
                    if (run) {
                        store.state.output = data.output
                    }
                    store.actions.freshList()
                }
            })
        },
        update: function (id, run = false) { //更新代码
            $.ajax({
                url: api.v1.code.update(id, run),
                type: 'PUT',
                data: {
                    code: store.state.code,
                    name: store.state.name
                },
                dataType: 'json',
                success: function (data) {
                    if (run) {
                        store.state.output = data.output
                    }
                    store.actions.freshList()
                }
            })
        },
        remove: function (id) { //删除代码
            $.ajax({
                url: api.v1.code.remove(id),
                type: 'DELETE',
                dataType: 'json',
                success: function (data) {
                    store.actions.freshList()
                }
            })
        }
    }
}

store.actions.freshList() // Store的初始化工作，先获取代码列表
```
相比我们之前结构，把统一的数据操作都放在 Store 中，这样就不会显得很混乱，并且 API 也简洁了不少。

下面改编写组件了。

在写代码的时候，我们需要按照“人类思维”来写代码，但是在具体组织代码的时候，我们需要按照“程序思维”来组织代码。根组件会引用前面的组件，但是前面的组件我们都还没有实现，所以根组件事实上是应该放在所有代码之后的。所以大家在写的时候注意自己代码的该写在哪里。不要代码全对而产生 `undefined` 错误。

先编写根组件：

`index.js`
```javascript
let root = new Vue({ //根组件，整个页面入口
    el: '#app',
    template: '<app></app>',
    components: {
        'app': app
    }
})
```

`app` 是我们的页面框架，我们在下面实现它。

然后在 root **上面** 编写页面框架：

`index.js`
```javascript
let app = { //整体页面布局
    template: `
        <div class="continer-fluid">
            <div class="row text-center h1">
                在线 Python 解释器
            </div>
            <hr>
            <div class="row">
                <div class="col-md-3">
                    <code-list></code-list>
                </div>
                <div class="col-md-9">
                    <div class="container-fluid">
                        <div class="col-md-6">
                            <p class="text-center h3">请在下方输入代码:</p>
                            <code-input></code-input>
                            <hr>
                            <code-options></code-options>
                        </div>
                        <p class="text-center h3">输出</p>
                        <div class="col-md-6">
                            <code-output></code-output>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    components: {
        'code-input': input,
        'code-list': list,
        'code-options': options,
        'code-output': output
    }
}
```
`app` 组件是所有组件被组织在一起的地方，但是用到的组件都还没有实现，所以还没有被实现的组件代码都应该放在它的 **上面**。

list 组件：

`index.js`
```javascript
let list = { //代码列表组件
    template: `
    <table class="table table-striped">
        <thead> 
            <tr>
                <th class="text-center">文件名</th> 
                <th class="text-center">选项</th> 
            </tr>
        </thead>
        <tbody>
            <tr v-for="item in state.list">
            <td class="text-center">{{ item.name }}</td>
            <td>
                <button class='btn btn-primary' @click="getDetail(item.id)">查看</button>
                <button class="btn btn-primary" @click="run(item.id)">运行</button>
                <button class="btn btn-danger" @click="remove(item.id)">删除</button>
            </td>
            </tr>
        </tbody> 
    </table>
    `,
    data() {
        return {
            state: store.state
        }
    },
    methods: {
        getDetail(id) {
            store.actions.getDetail(id)
        },
        run(id) {
            store.actions.runDetail(id)
        },
        remove(id) {
            store.actions.remove(id)
        }
    }
}
```

options 组件：

`index.js`
```javascript
let options = {//代码选项组件
    template: `
    <div style="display: flex;
         justify-content: space-around;
         flex-wrap: wrap" >
        <button class="btn btn-primary" @click="run(state.code)">运行</button>
        <button class="btn btn-primary" @click="update(state.id)">保存</button>
        <button class="btn" @click="update(state.id, true)">保存并运行</button>
        <button class="btn btn-primary" @click="newOptions">New</button>
    </div>
    `,
    data() {
        return {
            state: store.state
        }
    },
    methods: {
        run(code) {
            store.actions.run(code)
        },
        update(id, run = false) {
            if (typeof id == 'string') {
                store.actions.create(run)
            } else {
                store.actions.update(id, run)
            }
        },
        newOptions() {
            this.state.name = '';
            this.state.code = '';
            this.state.id = '';
            this.state.output = '';
        }
    }
}
```

input 组件：

`index.js`
```javascript
let input = { //代码输入组件
    template: `
    <div class="form-group">
        <textarea 
        class="form-control" 
        id="input"
        :value="state.code"
        @input="inputHandler"></textarea> 
        <label for="code-name-input">代码片段名</label>
        <p class="text-info">如需保存代码，建议输入代码片段名</p>
        <input 
        type="text" 
        class="form-control" 
        :value="state.name"
        @input="(e)=> state.name = e.target.value">
    </div>
    `,
    data() {
        return {
            state: store.state
        }
    },
    methods: {
        flexSize(selector) {
            let ele = $(selector);
            ele.css({
                'height': 'auto',
                'overflow-y': 'hidden'
            }).height(ele.prop('scrollHeight'))
        },
        inputHandler(e) {
            this.state.code = e.target.value;
            this.flexSize(e.target)
        }
    }
}
```

我们把之前的 `flexSize`直接复制粘贴过来了。这样做的好处是，和组件有关的东西都在组件内，而不需要去到处找。 

output 组件：

`index.js`
```javascript
let output = { //代码输出组件
    template: `
    <textarea disabled 
    class="form-control text-center">{{ state.output }}</textarea>
    `,
    data() {
        return {
            state: store.state
        }
    },
    updated() {
        let ele = $(this.$el);
        ele.css({
            'height': 'auto',
            'overflow-y': 'hidden'
        }).height(ele.prop('scrollHeight'))
    }
}
```

在这里我们选择了完全不同的动态大小方案。在 input 组件中，我们选择的是使用 input 事件来触发调整大小的函数。而在这里，我们选择在 output 组件**更新**完毕之后之后再触发这个函数。

`.$el` 是这个组件最外层的 html 标签。在这里就是我们的 `textarea` 标签了。

如果我们需要组件在更新完毕之后做什么事情，就在选项对象里定义 `updated` 属性，组件会在更新完毕后调用它。这属于组件的生命周期的一部分。

生命周期有点类似 Django 的信号系统。比如有的同学可能知道 `post_save` ，我们可以用它来让一个模型保存完毕之后做些事情。而组件则有许多这样的东西。
Vue 给我们提供了组件在不同阶段的接口。

关于生命周期更详细的细节，我们会在后面的章节里讨论。

到这里我们就完成了这次重构。赶紧试试效果吧。

---
本章我们初次接触了 DRF 和 Vue ，并且重构了一下试了试效果。DRF 则节约了我们不少接口开发的时间。vue 使我们的开发更加有调理，页面不再是一团乱麻。在下一章，我们将学习前端工具链。要一路从 node 学到 webpack 。





