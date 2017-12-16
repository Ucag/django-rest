#Django REST 系列教程（三）（上）
#你好 Django REST Framework
在第二章，我们学习了 REST 开发的基本知识，并且在没有借助任何框架的情况下
完成了我们的 RESTful APP 的开发，虽然我们已经考虑到了许多的情况，但是我们的 APP
依然有许多的漏洞。在本章，我们将会进入 **Vue** 和 **Django REST framework** 
的学习。本章将会分为三个部分，分别是：
    
- **你好 Django REST Framework**
- **你好 Vue**
- **重构 APP**

这就是我们的三个部分了。第一个部分学习 DRF ，第二个部分学习 Vue ，最后一个部分为实战部分。在上部分，我们会学习以下知识点：

1. 了解 DRF 的基本使用。
2. 了解并能灵活使用序列化器。

这个部分的知识点看起来很少，其实等大家真正进入他们的学习中时，会发现其中的知识点也不少。当然，这是一个教程，不是 DRF 官方文档复读机，所以一旦在看教程的过程中有什么不懂的地方，去查询 [DRF 文档](http://www.django-rest-framework.org/)是个好习惯。同时，本章也会涉及 python 的编程知识，由此可见，对于 web 后端的开发来说，语言的基础是多么重要。同样的，如果遇到在自己查资料之后还不懂的地方，评论留言或者提 [ISSUE](https://github.com/Ucag/django-rest)。

##准备工作
首先，我们需要安装 DRF ，在终端中运行：
```
pip install djangorestframework
```
创建一个新的项目：
```
python django-admin.py startproject api_learn
```
把路径切换到项目路径内，创建一个新的 APP ：
```
python manage.py startapp rest_learn
```
编辑你的 `settings.py` 文件，把我们的 APP 和 DRF 添加进去：
```
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_learn'
]
```
编辑 `rest_learn` 的 `models.py` ：
```python
from django.db import models
class TestModel(models.Model):
    name = models.CharField(max_length=20)
    code = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    changed_time = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return self.name
```
在 `DateTimeField` 是时间与日期字段，其中的参数意思是：

- `auto_now`: 在实例每次被保存的时候就更新一次值，在这里，我们把它作为修改值。所以 `changed_time` 字段的值会随着实例的每次修改和保存而发生变化，这样就可以记录实例的修改时间。
- `auto_now_add`: 在实例被创建的时候就会自动赋值。`created_time` 的值就会在实例被创建时自动赋值，这样我们就可以记录实例是在什么时候被创建的。

将我们的模型添加进管理站点。
编辑 `rest_learn` 下的 `admin.py`:
```python
from django.contrib import admin
from .models import TestModel

@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    pass
```
`admin.register` 是一个将 `ModelAdmin` 快速注册模型到管理站点的装饰器，其中的参数
是需要被注册的模型。

编辑 `api_learn` 下的  `urls.py`：

```python
from django.conf.urls import url, include
from django.contrib import admin
import rest_framework

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^drf-auth/',include('rest_framework.urls'))
]
```
第二个 `url` 配置用于提供登录的功能。

在项目路径下运行：
```
python manage.py makemigrations
python migrate
```
生成我们需要的数据库文件。

创建管理员。在终端中运行：
```
(root) λ python manage.py createsuperuser
Username (leave blank to use 'administrator'): admin
Email address:
Password:
Password (again):
Superuser created successfully.
```

在项目路径下创建两个空文件，分别是 `data.py`，`rest_test.py`。

`data.py` 主要用来为我们提供一些虚拟数据。

编辑 `data.py`。
```python
from django import setup
import os
os.environ.setdefault('DJAGNO_SETTINGS_MODULE','api_learn.settings') # 在环境变量中设置配置文件
setup() # 加载配置文件

from rest_learn.models import TestModel

data_set = {
    'ls':"""import os\r\nprint(os.listdir())""",
    'pwd':"""import os\r\nprint(os.getcwd())""",
    'hello world':"""print('Hello world')"""
}
for name, code in data_set.items():
    TestModel.objects.create(name=name,code=code)

print('Done')
```

直接运行 `data.py` ，当看到 Done 的时候就说明数据写入已经完成了。细心的同学已经发现了，这和我们第一章的 `单文件 Django` 很相似。记得我们在第一章说过的吗：

>使用前先配置

我们需要使用 Django 的模型，所以需要先配置它，在这里我们选择了使用第一章中的第二种方法来配置。如果你忘了第一章讲了些什么，快回去看看吧。这也是我们先讲 `单文件 Django` 原因所在，知道了配置方法之后，我们就不需要再打开 shell 十分不方便的编写代码了。

为了确保万无一失，大家可以选择登录进后台看看我们的数据是否写入了数据库。

本节剩下所有的代码都会在 `rest_test.py` 中进行，所以先编写好配置。

编辑 `rest_test.py`：
```python
from django import setup
import os

# 加载配置
os.environ.setdefault('DJAGNO_SETTINGS_MODULE','api_learn.settings')
setup()


```
准备工作已经完成了，让我们正式的开始学习。

##你好 Django REST Framework
在上一章的结尾我们知道我们的 APP 其实是不安全的，因为我们并没有对上传的数据进行任何的检查，这使得我们的应用随时暴露在被攻击的安全隐患之下。同时，由于我们的应用十分的小，我们并没有考虑到其它的“内容协商”，如果在今后的应用中我们需要用到 `xml` 格式的数据，那么我们又需要重新编写一次我们的代码。我们的应用代码不仅不安全，同时也不灵活。这一次，我们需要解决这个问题。


###序列化器
刚才我们说道，我们需要对上传的数据进行检查，按照一般的思路，我们一般会编写一大堆的 `if` 语句来判断上传的数据是否符合要求。用脚指头都可以知道这么做是最最笨的方法。再好一点的办法是编写一些工具函数来检查数据是否符合要求，比如我们的 `name` 字段的长度是小于 20 个字符的，数据类型是字符串。那我可以单独编写一个这样的函数：
```python
def validate_name(post_data):
    name = post_data.get('name')
    if isinstance(name, str):
        if len(name) <= 20:
            return name
    raise Exception('Invalid name data.')
```

这样我们直接在视图逻辑中直接调用这个函数就可以了。这个比单独写 `if` 语句要好一些了。但是依然会有不少问题，如果中途我们的 `name` 字段的长度被修改为 30 个字符了，那我们是不是要再改一次我们的 `validate_name` 函数呢？要是我们的 `name` 字段被修改成了 `code_name` ，那我们是不是还要再改一次呢？每一次的改动都会牵扯到 `validate_name` 的改动。 更要命的是，如果我们的数据类型发生了变化，由于前端传过来的数据都是字符串，我们需要对数据进行转换才可以保存到数据库中，这样就加大了我们的工作量。那有没有更好的办法呢？有，那就是我们的 `Serializer` ，也就是序列化器。

序列化器是什么？看它的名字我们就知道了，它是用来序列化数据的，我们在第二章知道了什么是数据的“序列化”，同时它也提供了对数据的验证功能，更棒的是，这个数据验证是双向的。也就是说，它既可以验证前端上传到后端的数据，它也可以验证后端传到前端的数据。前者比较好理解，那后者怎么理解呢？比如，我们前端需要的 `created_time` 字段的日期的格式为 '月-日-年' ，那么我们就可以在序列化器中写好，提前做好格式转换的工作，把验证通过数据传给前端。所以，我们序列化器的处理流程大概是这样的：
```
client ----> views <-----> serializer <-----> model
```
以及，序列化器还可以规定前端可以修改哪些字段，前端可以知道哪些字段。我们只希望客户端修改 `name` 和 `code` 两个字段，有的人可能会偷偷上传 `created_time` 字段，要是我们没有对它做拦截，我们的字段就会被随意修改啦，这样可不太好。

说的很抽象，我们来实际练习一下。接下来的所有代码都是在 `rest_test.py` 中进行的，大家接着刚才的代码写就行了。如果你对这些代码有任何的别扭的感觉，或者是“心头堵的慌”的感觉，或者是产生了任何“这样做好麻烦啊”之类的想法，请忍住，到后面你就明白了。

```python
from rest_framework import serializers

class TestSeriOne(serializers.Serializer):
    name = serializers.CharField(max_length=20)
```
这样我们就创建好了一个序列化器。对 Django Form 很熟悉的同学或许已经发现了，这不就很像是 Django 表单的写法吗？是的，事实上，序列化器用的就是表单的逻辑，所以如果你熟悉 Django Form 的 API ，那你上手序列化器也会很快。同时，序列化器和表单一样，拥有很多的字段，在之后的章节中我们会慢慢学习到它们，现在我们对字段的了解就先知道一点是一点。我们来使用一下我们的序列化器。
接着在下面写：
```python
frontend_data = {
        'name':'ucag',
        'age':18
    }

test = TestSerilOne(data=frontend_data)
if test.is_valid():
    print(test.validated_data)
```
我们假设有一个前端上传的数据为 `frontend_data` ，然后我们使用序列化器来验证上传的数据。它的使用方法和表单一样，想要获得合法的数据需要先运行 `.is_valid()` 方法，在运行这个方法后，如果验证通过，合法的数据就会被保存在 `.validated_data` 属性中。现在直接运行我们的 `rest_test.py` 脚本试试。不出意外的话，你会看到这个结果：
```
OrderedDict([('name', 'ucag')])
```
我们可以看到，`age` 字段被序列化器给过滤掉了，这样就可以防止前端上传一些奇奇怪怪的字段了。我们把刚才的序列化器修改一下，改成这个样子：
```python
class TestSerilOne(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    age = serializers.IntegerField()
```
我们新增加了一个字段。把我们的 `frontend_data` 改成这个样子：
```python
frontend_data = {
        'name':'ucag',
        'age':'18'
    }
```
其它什么都不变，运行 `rest_test.py` ，输出变成了这样：
```
OrderedDict([('name', 'ucag'), ('age', 18)])
```
好像没什么不一样。。。再仔细看看？看看 `age` 变成了什么？我们传进去的数据是个字符串，但是在经过验证之后，它的类型就变成了整数型！让我们来看看，故意给它传错误的数据会发生什么。
把 `frontend_data` 改成这样：
```python
frontend_data = {
        'name':'ucag',
        'age':'ucag'
    }
```
把之前的测试改成这样：
```python
test = TestSerilOne(data=frontend_data)
if not test.is_valid():
    print(test.errors)
```
输出应该是这样的：
```
{'age': ['A valid integer is required.']}
```
序列化器把不符合要求的字段的错误信息给放在了 `.errors` 属性里。我们可以通过这个属性来查看相应的错误信息，在前端上传的数据出错的时候我们就可以直接把这个错误直接发送给前端，而不用自己手写错误信息了。

刚刚体验的是验证前端的数据，现在我们来看看序列化器是怎么验证后端数据的。假设前端现在只想知道 `name` 字段的信息，比如我们之前 APP 项目的代码列表，我们需要显示的仅仅就是代码片段的名字。现在就需要对后端数据做验证了。

注释掉刚才做实验的代码，接着在下面再创建一个序列化器：
```python
# test = TestSerilOne(data=frontend_data)
# if not test.is_valid():
#     print(test.errors)

class TestSerilTwo(serializers.Serializer):
    name = serializers.CharField(max_length=20)

```
现在我们来使用它来验证后端的数据，在下面接着写：
```python
from rest_learn.models import TestModel
code = TestModel.objects.get(name='ls')
test = TestSerilTwo(instance=code)
print(test.data)
```
运行 `rest_test.py` ，你的输出会是这样的：
```
{'name': 'ls'}
```
我们从模型中获取了一个模型实例，然后通过 `instance` 参数把它放进了序列化器里，然后，我们通过 `.data` 属性来访问验证之后的数据。可以看到，只有 `name` 字段被提取了出来，`code`、`created_time`、`changed_time` 字段都没有出现在提取之后的数据里。真的是很方便呀，那我想提取所有的模型实例该怎么办呢？因为前端的代码列表需要的是所有实例的名字信息啊。把我们之前做验证的代码改成这样：
```python
from rest_learn.models import TestModel
codes = TestModel.objects.all()
test = TestSerilTwo(instance=codes,many=True)
print(test.data)
```
你会看到输出是这个样子的：
```
[OrderedDict([('name', 'hello world')]), OrderedDict([('name', 'pwd')]), OrderedDict([('name', 'ls')])]
```
此时的 `.data` 属性变成了一个列表。我们提取了所有的模型实例，通过 `instance` 参数传递进了序列化器，通过 `many=True` 参数设置告诉序列化器我们传进去的是一个查询集实例，这样序列化器就会自己做相应的处理了。是不是特别方便？

到目前为止，我们的序列化器都是一个个字段手写出来的，通常，我们序列化的字段和模型的字段是统一的，那能不能通过模型来生成我们的序列化器呢，就像模型表单那样？当然是可以的。
注释掉之前的验证代码，接着在后面写：
```python
# from rest_learn.models import TestModel
# codes = TestModel.objects.all()
# test = TestSerilTwo(instance=codes,many=True)
# print(test.data)

from rest_learn.models import TestModel
class TestSerilThree(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ['name','code','created_time','changed_time','id']
        read_only_fields = ['created_time','changed_time']
```
这一次，我们继承的是 DRF 的模型序列化器，通过 `Meta` 给模型序列化器传模型，通过 `fields` 来告诉序列化器我们需要序列化哪些字段。那 `read_only_fields` 又是用来干什么的呢？

刚才我们说过，序列化器是双向验证的，对前端和后端都有验证。有时后端不希望某些字段被前端修改该，这就导致了我们对前端和后端的序列化字段会有所不同。一旦字段发生了变化，也就意味着序列化器也会发生变化，那该怎么办呢？那就是把我们不希望前端修改的字段放在 `read_only_fields` 选项里，这样，当序列化器在序列化前端的字段时，即便是前端有这些字段，序列化器也会忽略这些字段，这样就可以防止别有用心的人暴力修改我们的字段。

好像还不是很懂？别着急，我们先用它试试看，接着在下面写：
```python
code = TestModel.objects.get(name='ls')
codes = TestModel.objects.all()

# 前端写入测试
frontend_data = {
    'name':'ModelSeril',
    'code':"""print('frontend test')""",
    'created_time':'2107-12-16'
}
test1 = TestSerilThree(data=frontend_data)
if test1.is_valid():
    print('Frontend test:',test1.validated_data)
# 后端传出测试：
test2 = TestSerilThree(instance=code)
print('Backend single instance test:',test2.data)
test3 = TestSerilThree(instance=codes,many=True)
print('Backend multiple instances test',test3.data)
```
输出应该是这样的：
```
Frontend test: OrderedDict([('name', 'ModelSeril'), ('code', "print('frontend test')")])

Backend single instance test: {'created_time': '2017-12-16T05:16:12.846759Z', 'name': 'ls', 'code': 'import os\r\nprint(os.listdir())', 'id': 3, 'changed_time': '2017-12-16T05:16:12.846759Z'}

Backend multiple instances test [OrderedDict([('name', 'hello world'), ('code', "print('Hello world')"), ('created_time', '2017-12-16T05:16:12.815559Z'), ('changed_time', '2017-12-16T05:16:12.815559Z'), ('id', 1)]), OrderedDict([('name', 'pwd'), ('code', 'import os\r\nprint(os.getcwd())'), ('created_time', '2017-12-16T05:16:12.831159Z'), ('changed_time', '2017-12-16T05:16:12.831159Z'), ('id', 2)]), OrderedDict([('name', 'ls'), ('code', 'import os\r\nprint(os.listdir())'), ('created_time', '2017-12-16T05:16:12.846759Z'), ('changed_time', '2017-12-16T05:16:12.846759Z'), ('id', 3)])]
```
我们可以看到，模型序列化器正确的序列化了我们的模型实例，包括其中的 `DateTimeField` 字段，如果是我们手写来处理，不知道会有多麻烦。

我们先看前端写入的测试的输出，虽然我们的 `frontend_data` 有一个 `created_time` 字段，但是在最后的 `.validated_data` 中根本就没有它的身影，我们的序列化器成功的过滤掉了这个非法字段。

再看后端传出测试输出，模型实例和查询集实例的输出结果都很正常。最重要的是，`created_time` 和 `changed_time` 两个字段是被正常序列化了的，这两个字段并没有受到 `read_only_fields` 的影响，所以前端只能看到这个字段，不能修改这个字段。

这样就方便许多了！接下来我们进入序列化器的进阶学习。

刚刚的序列化器结构都很简单，使用起来也很简单，要是有关系字段该怎么处理呢？我并不打算直接用模型序列化器来讲解，因为模型序列化器都帮我们把工作都完成了，我们最后什么都看不到。所以然我们来手写一个能处理关系字段的序列化器。在开始之前，注释掉之前的实验代码：
```pyton
# code = TestModel.objects.get(name='ls')
# codes = TestModel.objects.all()

# 前端写入测试
# frontend_data = {
#     'name':'ModelSeril',
#     'code':"""print('frontend test')""",
#     'created_time':'2107-12-16'
# }
# test1 = TestSerilThree(data=frontend_data)
# if test1.is_valid():
#     print('Frontend test:',test1.validated_data)
# 后端传出测试：
# test2 = TestSerilThree(instance=code)
# print('Backend single instance test:',test2.data)
# test3 = TestSerilThree(instance=codes,many=True)
# print('Backend multiple instances test',test3.data)
```
在开始编写之前，我们需要搞懂一个问题，序列化器到底是什么？它用起来的确很方便，但是当我们遇到问题时却不知道从何下手，就像刚才的问题，如何利用序列化器处理关系字段？如果你去查看官方文档，官方文档会告诉你，使用 `PrimaryKeyRelatedField` ，我相信第一次看到这个答案的你一定是一脸懵逼，为什么？？？为什么我的关系模型就成了一个字段了？？？？我明明想要的是关系模型相关联的实例对象啊。。。你知道 `PrimaryKeyRelatedField` 是关系模型的主键。比如我们的 `TestModel` 和 `User` 表是关联的，如果我使用的是 `PrimaryKeyRelatedField` 字段，那序列化的结果出来就会是类似这样的：
```python
{
    user:1,
    code:'some code',
    name:'script name' 
}
```
和 `TestModel` 相关联的 `User` 实例就变成了一个主键，我们可以通过访问这个主键来访问 `User` 与 `TestModel` 相关联的实例。但是一般，我们想要的效果是这样的：
```python
{
    user:{
        'id':1,
        'email':'email@example.com',
        'name':'username'
    },
    code:'some code',
    name:'script name'
}
```
我们想要的是 `User` 实例的详细信息，而不是再麻烦一次，用 `PrimaryKeyRelatedField` 的值再去查询一次。而且更头痛的是，如果使用 `PrimaryKeyRelatedField`, 在创建实例的时候，你必须要先有一个相关联的 `User` ，在创建 `TestModel` 时候再把这个 `User` 的主键给传进去。也就是说，你不能一次性就创建好 `TestModel` 和 `User` ，要先创建 `User` 再创建 `TestModel`，这个流程简直是让人头皮发麻。如果我们想一次性创建好他们该怎么办呢？如果有心的同学去看看 DRF 的 release note ，就会知道，把 `User` 模型的序列化器当作一个字段就行了。什么？？？序列化器当成一个字段？？？这种操作也可以？？从来没见过这种操作啊。。在 Django 表单中也没有见过这种操作啊。。怎么回事啊？？

淡定，同样的，我们先来做个实验，先体验下“序列化器当作字段”是怎么回事。假设我们希望能在创建 `User` 的同时也能够同时创建`Profile`。 在 `rest_test.py` 下面接着写：
```python
class ProfileSerializer(serializers.Serializer):
    tel = serializers.CharField(max_length=15)
    height = serializers.IntegerField()

class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    qq = serializers.CharField(max_length=15)
    profile = ProfileSerializer()
```
我们可以看到，`UserSerializer` 的 `profile` 字段是 `ProfileSerializer` 。现在我们使用下这个序列化器。接着在下面写：
```python
frontend_data = {
    'name':'ucag',
    'qq':'88888888',
    'profile':{
        'tel':'66666666666',
        'height':'185'
    }
}

test = UserSerializer(data=frontend_data)
if test.is_valid():
    print(test.validated_data)
```
我们可以看到输出是这样的：
```
OrderedDict([('name', 'ucag'), ('qq', '88888888'), ('profile', OrderedDict([('tel', '66666666666'), ('height', 185)]))])
```
可以看到，我们的字段都被正确的序列化了。我们同时创建了 `User` 和 `Profile` 。并且他们也是正确的关联在了一起。

现在可以问，这是怎么回事呢？这是因为序列化器其实就是一个特殊的“序列化器字段”。怎么理解呢？再说的容易懂一点，因为序列化器和序列化字段都是 python 的同一种数据结构——描述符。那描述符又是什么东西呢？官方文档是这么说的：

>In general, a descriptor is an object attribute with “binding behavior”, one whose attribute access has been overridden by methods in the descriptor protocol. Those methods are `__get__()`, `__set__()`, and `__delete__()`. If any of those methods are defined for an object, it is said to be a descriptor.

>一般地，描述符是拥有“绑定行为”的对象属性，当这个属性被访问时，它的默认行为会被描述符内的方法覆盖。这些方法是 `__get__()`, `__set__()`, `__delete__()` 。任何一个定义的有以上方法的对象都可以被称为描述符。

说的太绕了，我们来简化一下。

1. 描述符是有默认行为的属性。
2. 描述符是拥有  `__get__()`, `__set__()`, `__delete__()` 三者或者三者之一的对象。

所以，描述符是属性，描述符也是对象。

我们先来理解第一条。描述符是属性。什么是属性呢？对于 `a.b` 来说，`b` 就是属性。这个属性可以是任何东西，可以是个方法，也可以是个值，也可以是任何其它的数据结构。当我们写 `a.b` 时就是在访问 `b` 这个属性。
再理解第二条。描述符是对象。对象是什么呢？通常，我们都是使用 `class` 来定义一个对象。根据描述符定义，有 `__get__()`, `__set__()`, `__delete__()` 之一或全部方法的对象都是描述符。

满足以上两个条件，就可以说这个对象是描述符。

一般地，`__get__()`, `__set__()`, `__delete__()` 应该按照如下方式编写：
```
descr.__get__(self, obj, type=None) --> value

descr.__set__(self, obj, value) --> None

descr.__delete__(self, obj) --> None
```

一般地，描述符是作为对象属性来使用的。

当描述符是一个对象的属性时，如 `a.b` ，`b` 为一个描述符，则执行`a.b` 相当于执行`b.__get__(a)`。 而 `b.__get__(a)` 的具体实现为 `type(a).__dict__['b'].__get__(a, type(a))` 。以上这个过程没有为什么，因为 python 的实现就是这样的。我们唯一需要理解的就是，为什么会这样实现。首先我们需要读懂这个实现。

假设，`a.b` 中，`a` 是 `A` 的子类，`b` 是描述符 `B` 的实例。

1. `type(a)` 返回的是 `a` 的类型 `A`。那就变成了 `A.__dict__['b'].__get__(a, type(a))` 。

2. `A.__dict__['b']` 返回的是 `A` 的**类属性** `b` 的值。假设 `A.__dict__['b']` 的值为 `Ab`，那么就变成了 `Ab.__get__(a, type(a))`。

    我们在这里暂停一下。注意 **`A.__dict__['b']` 返回的是 `A` 的类属性**，`b` 的值是一个描述符，也就是说，`Ab` 是个描述符。那么连起来，就变成了：
    
    - `Ab` ，也就是 `b` ，是一个**类属性**，这个类属性是个描述符。也就是**描述符** `B` 的实例**是** `A` 的**类属性**。
    
3. 最后一步就很简单了，就是调用描述符的 `__get__()` 方法，也就是 `Ab.__get__(a, A)`，也就是 `b.__get__(a, A)` 。到这里，大家可能会问一个问题，`__get__` 的参数也就是 `a` 和 `A` 是谁传进去的呢？，答案说出来很简单，但是很多时候有的同学容易绕进去就出不来了。答案就是：
python 解释器自己传进去的。就像是类方法的 `self` 一样，没谁手动传 `self` 进去，这都是 python 的设计者这样设计的。

一句话总结一下。 **当 `b` 为 `A` 类属性且为描述符时，`A` 的实例 `a` 对于 `b` 访问也就是`a.b` 就相当于 `b.__get__(a, A)`。**所以，此时，对于 `b` 属性的访问结果就取决于 `b` 的 `__get__()` 返回的结果了。

我们稍微再推理一下，就可以知道，如果一个对象的**属性**是描述符**对象**，而且这个对象本身也是描述符的话，那么，这个对象的各种子类就可以相互作为彼此的属性。说的很复杂，举个简单的例子。

我们来简单的运用下刚才学到的知识，在解释器里输入以下代码：
```
In [1]: class Person: # 定义 Person 描述符
   ...:     def __init__(self, name=None):
   ...:         self.name = name
   ...:     def __set__(self, obj, value):
   ...:         if isinstance(value, str):
   ...:             self.name = value
   ...:         else:
   ...:             print('str is required!')
   ...:     def __get__(self, obj, objtype):
   ...:         return 'Person(name={})'.format(s
   ...: elf.name)
   ...: class Dad(Person):
   ...:     kid = Person('Son')
   ...: class Grandpa(Person):
   ...:     kid = Dad('Dad')
   ...:
   ...: dad = Dad('Dad')
   ...: gp = Grandpa('Granpa')
   ...:
   ...: print("Dad's kid:",dad.kid)
   ...: print("Grandpa's kid:",gp.kid)
   ...:
Dad's kid: Person(name=Son)
Grandpa's kid: Person(name=Dad)

In [2]: dad.kid = 18
str is required!

In [3]: dad.kid
Out[3]: 'Person(name=Son)'
```
可以看到，我们在定义描述符之后，除了直接实例化使用他们之外，还把他们作为其它描述符的属性。描述符 `Dad` 的属性 `kid` 也是一个描述符。 我们的对 `kid` 的赋值成功被 `__set__` 拦截，并在赋值类型不规范时给出了我们事先写好的警告，并且原来的值也没有被改变。

现在我们回到序列化器中来。序列化器和序列化器字段就是像这样的描述符，他们完全是同一种东西。所以他们完全可以作为彼此的类属性来使用。一旦明白了这一点，就可以有各种“骚操作”了。序列化器最基本的字段描述符定义了字段的操作，所以不用我们自己重新去编写 `__get__` `__set__` `__delete__` ，DRF 已经编写好基本的逻辑，我们只需要调用现成的接口就可以实现自定义字段。在简单的继承 `serializers.Field` 后就可以使用这些现成的接口了，这个接口是：
`.to_representation(obj)` 和 `.to_internal_value(data)` 。

- `.to_representation(obj)`: 它决定在访问这个字段时的返回值应该如何展示，obj 是 `to_internal_value` 返回的对象。 作用如同描述符的`__get__`。应该返回能够被序列化的数据结构。如数字，字符串，布尔值 `date`/`time`/`datetime` 或者 `None` 。
- `.to_internal_value(data)`: 它决定在对这个字段赋值时应该进行的操作，data 是前端传过来的字段值。作用如同描述符的`__set__` 操作，应该返回一个 python 数据结构。在发生错误时，应抛出 `serializers.ValidationError`。

我们现在可以自己定义一个字段试试看，注释掉之前的测试，接着 `rest_test.py` 写：
```python
# frontend_data = {
#     'name':'ucag',
#     'qq':'88888888',
#     'profile':{
#         'tel':'66666666666',
#         'height':'185'
#     }
# }

# test = UserSerializer(data=frontend_data)
# if test.is_valid():
#     print(test.validated_data)
class TEL(object):
    """电话号码对象"""
    def __init__(self, num=None):
        self.num = num
    def text(self, message):
        """发短信功能"""
        return self._send_message(num, message)
    def _send_message(self,message):
        """发短信"""
        print('Send {} to {}'.format(message[:10], self.num))
class TELField(serializers.Field):
    def to_representation(self, tel_obj):
        return tel_obj.num
    def to_internal_value(self, data):
        data = data.lstrip().rstrip().strip()
        if 8 <= len(data) <=11:
            return TEL(num=data)
        raise serializers.ValidationError('Invalid telephone number.')
```
这样就完成了我们的“骚操作”字段。我们就可以这样使用它，接着在下面写：
```python
class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    tel = TELField()

frontend_data = {
    'name':'ucag',
    'tel':'88888888'
}
test = ContactSerializer(data=frontend_data)
if test.is_valid():
    tel = test.validated_data['tel']
    print('TEL',tel.num)
    tel.text('这是一个骚字段')
```
直接运行 `rest_test.py`，输出如下：
```
TEL 88888888
Send 这是一个骚字段 to 88888888
```
我们自定义的字段就完成了。

以上就是我们对序列化器的学习。目前我们就学习到这个程度，序列化器剩下知识的都是一些 API 相关的信息，需要用到的时候直接去查就是了。我们已经明白了序列化器的原理。以后遇到什么样的数据类型处理都不怕了，要是遇到太奇葩的的需求，大不了我们自己写一个字段。相关的细节我们在以后的学习中慢慢学习。

###API View 与 URL 配置
这是 DRF 的又一个很重要的地方，在第二章，我们自己编写了 APIView ，并且只支持一种内容协商，DRF 为我们提供了功能更加完备的 APIView, 不仅支持多种内容协商，还支持对 API 访问频率的控制，对查询结果过滤等等。

DRF 的 API 视图有两种使用方式，一种是利用装饰器，一种是使用类视图。

我们主要讲类视图 API ，装饰器放在后面作为补充。

我们知道 Django 的视图返回的是 `HttpResponse` 对象，并且默认接收一个 `HttpRequest` 对象，我们可以通过这个请求对象访问到请求中响应的数据。同样的，DRF 的 APIView 也是接收一个默认的请求对象，返回一个响应对象。只是在 APIView 中的请求和响应对象变成了 DRF 的请求和响应对象。

DRF 的请求对象功能比 Django 自带的要完备很多，也强大很多。不仅原生支持 `PUT` 方法，还支持对 `POST` URL 的参数解析等众多功能。

我们来看看 DRF 的请求对象都有哪些功能：

1. `.data`: DRF 请求对象的 `data` 属性包含了所有的上传对象，甚至包括文件对象！也就是说，我们可以只通过访问 `resquest.data` 就能得到所有的上传数据，包括 `PUT` 请求的！还支持多种数据上传格式，前端不仅可以以 form 的形式上传，还可以以 `json` 等众多其它形式上传数据！
2. `.query_params`: `query_params` 属性包含了所有的 URL 参数，不仅仅是 GET 请求的参数，任何请求方法 URL 参数都会被解析到这里。
3. `.user`: 和原生的 `user` 属性作用相同。
4. `.auth`： 包含额外的认证信息。

当然，DRF 的请求对象不止有这些功能，还有许多其它的功能，大家可以去文档里探索一下。

DRF 的响应对象：

DRF 响应对象接收以下参数：
1. `data`: 被序列化之后的数据。将被用作响应数据传给前端。
2. `status`: 状态码。
3. `headers`: 响应头。
4. `content_type`: 响应类型。一般不需要我们手动设置这个字段。

让我们来看看 DRF 的 APIView 具体的应用方法：

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()
class ListUsers(APIView):
    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
```
这就是最简单的 APIView 了。我们的 `get` 函数的 `format` 参数是用于控制和前端的内容协商的，我们可以通过判断这个值来决定返回什么样类型的数据。同时，`APIView` 还有许多其它的参数供我们使用，但是目前我们就暂时先了解到这里。

别忘了，我们学习的是 REST 开发，对应的请求有对应普适的规则。所以，在 APIView 基础之上的类视图是十分有用的——`GenericView`，它就相当与我们之前编写的加了各种 Mixin 操作的 APIView，只不过 `GenericView` 提供的操作和功能比我们自己编写的要丰富很多。同样的，`GenericView` 也是通过提供各种通用使用各种 `Mixin` 的类属性和方法来提供不同的功能。所以我们就在这里简单的介绍一下这些类属性和方法：

`GenericView` 提供的属性有：

1. `queryset`: 和我们的 `APIView` 中的 `queryset` 作用是相同的。
2. `serializer_class`: 序列化器，`GenericView` 将会自动应用这个序列化器进行相应的数据处理工作。
3. `lookup_field`: 和我们之前编写的 `lookup_args` 作用相同，只是它只有一个值，默认为 'pk' 。
4. `lookup_url_kwarg`： 在 URL 参数中用于查询实例的参数，在默认情况下，它的值等于 `lookup_field`。
5. `pagination_class`: 用于分页的类，默认为 `rest_framework.pagination.PageNumberPagination`，如果使它为 `None` ，就可以禁用分页功能。
6. `filter_backends`: 用于过滤查询集的过滤后端，可以在 `DEFAULT_FILTER_BACKENDS` 中配置。

提供的方法有：

1. `get_queryset(self)`: 获取查询集，默认行为和我们编写的 `get_queryset` 相同。
2. `get_object(self)`: 获取当前实例对象。
3. `filter_queryset(self, queryset)`: 在每一次查询之后都使用它来过滤一次查询集。并返回新的查询集。
4. `get_serializer_class(self)`: 获取序列化器，可以通过编写这个方法做到动态的序列化器的更换。
5. `get_serializer_context(self)`: 返回一个作用于序列化器的上下文字典。默认包含了 `request`, `view`,`format` 键。如果这里不懂没关系，我们后面还会讲到。

当然，`GenericView` 还提供了许多其它的功能，所以想要更多了解的同学可以去查阅官方文档。没看的也不用担心，我们在之后会慢慢的涉及到更多的知识点。

以上都介绍的很简单，我们要重点介绍的是下面的 `ViewSet`。
什么是 `ViewSet` ，`ViewSet` 顾名思义就是一大堆的视图集合。为什么要把一大推的视图集合到一起呢？因为他们都是通用的。具体体现在哪些地方呢？他们都是符合 REST 规范的视图，所以只需要按照 REST 规范就可以使用这些视图了。

比如，像这样，这是官方文档的例子：
```python
# views.py
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from myapps.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# urls.py
user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})
```
看，我们使用了 `ViewSet` 之后就不用手动的编写 `get` 等等方法了，只需要编写对应的操作函数就可以了。更让人惊喜的是，`ViewSet` 的使用方法和我们之前使用了 `MethodMapMixin` 的 `APIView` 是一模一样的。通过方法映射到具体的操作函数上来。但是含有比这样写更酷的方法：
```python
# urls.py
from myapp.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')
urlpatterns = router.urls
```
通过使用 `Router` 来自动生成我们需要的 API 接口。这个等会儿再说。我们先说说 `GenericViewSet` 和 `ModelViewSet` 。
`GenericViewSet`: 只是简单的添加上了 `GenericView` 的功能。我们重点说 `ModelViewSet`。
如果我们想要提供的 API 功能就是默认符合 REST 规范的 API ,要是使用 `ModelViewSet` 的话，我们就只需要提供一个参数就可以解决所有问题：
```python
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
```
是的，我们的视图就这样就写完了。简化到两行，要是你愿意，也可以简化到一行。再配合 `Router` 使用，一共不超过十行代码就可以完成我们之前写了好几百行的代码完成的功能。

这里我们只是做简单的了解，等到真正需要用的时候大家才可以学习到其中的奥妙。我们接下来说说 `Router` 。

`Router` 是用来帮我们自动生成 REST API 的。就像这种：
```python
url(r'^users/$', name='user-list'),
url(r'^users/{pk}/$', name='user-detail'),
url(r'^accounts/$', name='account-list'),
url(r'^accounts/{pk}/$', name='account-detail')
```
自动生成这些 API ，这些 API 都符合 REST 规范。

`Router` 的使用要结合我们上面学到的知识，本节我们就以 `Roter` 的使用收尾。

注释掉之前的验证代码，接着在后面写：
```python
# frontend_data = {
#     'name':'ucag',
#     'tel':'88888888'
# }
# test = ContactSerializer(data=frontend_data)
# if test.is_valid():
#     tel = test.validated_data['tel']
#     print('TEL',tel.num)
#     tel.text('这是一个骚字段')

from rest_framework.viewsets import ModelViewSet
class TestViewSet(ModelViewSet):
    queryset = TestModel.objects.all()

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'codes', TestViewSet)
urlpatterns = router.urls
print(urlpatterns)
```
使用过程不多说，都是机械式的使用，先使用 `register` 注册 url，第一个参数是 url 的前缀，就是想用什么开头，比如 `url(r'^users/$', name='user-list')` 就是以 `users` 开头。视图的名字 `Router` 会自己帮你加上，就两种名字。一个是 `<prefix>-list`，一个是`<prefix>-detail` 。当然，如果你想改也是可以改的。这个留到我们以后说。

直接运行 `rest_test.py` ，你应该会看到以下输出。
```
[<RegexURLPattern testmodel-list ^codes/$>, 
<RegexURLPattern testmodel-list ^codes\.(?P<format>[a-z0-9]+)/?$>, 
<RegexURLPattern testmodel-detail ^codes/(?P<pk>[^/.]+)/$>, 
<RegexURLPattern testmodel-detail ^codes/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$>, 
<RegexURLPattern api-root ^$>, <RegexURLPattern api-root ^\.(?P<format>[a-z0-9]+)/?$>]
```
这就是 `Router` 为我们生成的 API 了。细心的同学或许已经发现了，还有个 `api-root` 的视图，访问这个 API 会返回所有的 list 视图的 API 。可以通过这些链接访问到所有的实例。

---
我们对 DRF 的初步学习就到这里。很明显，我们的本节的重点就是序列化器，所以大家务必掌握序列化器的相关知识点，对视图和 URL 配置不是怎么懂都没有什么大的问题，这些都只是 DRF API 调用的问题，唯独序列化器的使用和原理需要大家十分扎实的掌握。所以，最低的要求是起码在本节结束后看到使用 DRF 的代码，能够明白它是什么意思，能够模仿着写出东西，最好能够举一反三。本节涉及的知识点的确有些难，不过一个星期理解这些知识点的时间也应该足够了。下一节我们就要开始 `Vue` 的学习，相对来说会轻松一些了。大家加油














































