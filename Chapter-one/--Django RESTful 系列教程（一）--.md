# **Django RESTful 系列教程（一）**
---
这是一个关于 Django RESTful 开发的教程。教程将会持续更新，更新进度为每个星期一篇。我们将会学习 **Django RESTful** 开发。在你阅读这个系列的教程之前，你需要注意这些：
>* 笔者用的是 python3.5 ，Django 1.11
>* 熟练 **python** 的使用。当文中提到**装饰器**或者**类**等概念时，请有最基本的映像。了解 **JavaScript** 的基本使用。
>* 在跟随教程的任何过程中，有任何问题，大家可以评论留言，或者给我发邮件 **1130195942@qq.com** ,或者是在 [github](http://github.com/Ucag/django-rest) 上提 issue。
>* 所有的代码和教程的 MakrDown 文本都可以在 [github](http://github.com/Ucag/django-rest)上找到。欢迎大家 clone 或者 star 。
>* 以前做过 Django 的相关项目，对 Django 有一定的了解，至少完成过官方的入门教程。在讲到 **模型** 、**视图** 等概念时，有一定的了解。从一定程度上来说，这也是一个进阶的教程。
>* 在本教程的最后，我们将会使用 **Django**、**Django REST framework**、**Vue**、**Vue-Router** 来做一个前后端分离的项目，也就是说，这篇教程会包含前端的内容，如果你对前端不了解也没关系，在拥有最基本的基础之上，大胆跟教程走可以了。
###转载请联系 **1130195942@qq.com**
---
### **本章概要：**
很多的 web 框架都以方便使用而著称，特别是 `flask` ，一个文件就可以做一个 Hellow world 了，那 `django` 可以吗？答案时肯定的。同时，我们将会简单的了解下 REST 的概念 。最后，我们将会利用我们才学的知识来编写我们的第一个 REST 项目

>* 单文件 **django** 
>* REST 是什么
>* 第一个 Django REST 项目。

---
## **单文件 Django**

### **发生了什么？**

相信大家对 Django 有一定的了解，对构建项目的每个过程也已经非常清楚了。总是重复的那么几个步骤：

1. 先运行 `django-admin startproject <your-project>` 创建项目
2. 再切换到项目路径下运行 `python manage.py startapp <your-app>`，创建项目的 app 。
3. 在每个 App 里写代码，写完了最后想要运行项目时运行 `python manage.py runserver` 来启动本地的开发服务器。

有的时候，我们仅仅是想做个实验，仅仅时想看看刚才手动写入的数据到底有没有正确写入或者是看看我的视图反响解析出来到底是什么样子。更重要的是，我们不想每次需要查看一些相关数据时，都需要从 app 目录里切出来，然后 `runserver` 。或许你会辩驳说，我们有 django 提供的 `shell` 可用，这样也可以很方便的和我们的应用交互。那么能不能再简单一点？换句话说，我们能不能直接执行我们当前编写的脚本呢？

 新建一个文件夹，叫做 `test-project` 。并在里面创建一个新的文件 `test.py` 。你的目录结构大概是这样的：

<pre>
test/
    test.py
</pre>

在开头引入这些包：

`test.py`

```python
from django.conf import settings 
from django.http import HttpResponse
from django.conf.urls import url
```

我们依次来看看他们都是什么意思。

**`from django.conf import settings`**：

`settings` 是 django 的配置文件钩子，你可以在项目的任何地方引入它，可以通过 `.` 路径符来访问项目的配置。比如 `settings.ROOT_URLCONF` 就会返回根 url 配置。关于钩子，我需要多说两句。讲道理，如果需要引用项目配置，标准的写法难道不应该是 `import project.settings as settings` 吗，这样才能连接到项目的配置啊，为什么我只是引入 django 自己的配置就可以了呢。这就是 django 的神奇之处了，在一切都还没有运行之前，django 首先做的就是加载配置文件，并且把 `settings` 对象的属性连接到各个配置上。注意，`settings` 是个对象，所以像 `from django.conf.settings import DEBUG` 之类的语法是错误的。因为它不是个模块。所以在访问配置时，只能以 `settings.<key>` 的形式来调用配置。

首先加载配置文件是一件天经地义的事情，只有知道了各个部分的配置如何，相应的功能才能按照需求运转。请大家记住这一点，这非常重要。在 django 中，加载配置文件有两种方式：

>第一种是使用 `settings.configure(**settings)`
手动的写每一项配置，这样做的好处是，如果你需要配置的东西不多，那就不单独再建个文件作为配置文件了。

>第二种是使用 `django.setup()` 
这是通过环境变量来配置的方法。
`django.setup()`  方法会自己查询环境变量 'DJANGO_SETTINGS_MODULE` 的值，会把它的值作为配置文件的路径，并读取这个文件的配置。

以上两种方法都可以用来配置 django 。我们这里采用第一种。注意，两种方式必须用一种，也就是说，想要使用 django ，必须对 django 进行配置。

**`from django.http import HttpResponse`**

用于返回一个响应。

**`from django.conf.urls import url`**
用于配置 urlpatterns 。

首先，让我们来编写配置，在 `test.py`下一行接着写:

`test.py`

```python
setting = {
    'DEBUG':True,
    'ROOT_URLCONF':__name__
}

settings.configure(**setting)
```

我们只是进行了简单的配置，设置 `DEGUB` 为 `True` 是因为我们想要在出错时能看到错误报告。设置 `ROOT_URLCONF` 为 `__name__` 也就是这个文件本身，也就是说，我们打算把 `urlpatterns` 这个变量写进这个文件中。

这个配置很简单吧。

接下来让我们编写视图，在 `test.py` 加入以下代码：

`test.py`

```python
def home(request):
    return HttpResponse('Hello world!')
```
这个视图非常简单，仅仅是返回一个字符串。

最后，把 `urlpatterns` 写在下面：

`test.py`

```python
urlpatterns = [url('^$',home,name='home')]
```

到目前为止，你的代码应该是这样的：

`test.py`

```python
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls import url
setting = {
    'DEBUG':True,
    'ROOT_URLCONF':__name__
}

settings.configure(**setting)

def home(request):
    return HttpResponse('Hello world!')

urlpatterns = [url('^$',home,name='home')]
```

该如何运行呢？一般情况下，我们是用 `manage.py` 来运行的。那 `manage.py` 又是怎么运行的？在 `manage.py` 内部，它调用了 django 的 `exute_from_command_line(**command_line_args)` 方法来运行我们的应用，所以，把这部分代码添加到最后（实际上，这是从 `manage.py` 复制粘贴过来的，去掉了不必要的部分，大家也可以这么做，嘿嘿嘿）：

`test.py`

```python
if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
```

此时，你的代码应该长这样：

`test.py`
```python
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls import url
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
```
回到 `test` 目录下，在终端运行 `python test.py runserver` ，然后在浏览器访问 `127.0.0.1:8000` ，不出意外的话，你会看到浏览器上有个 `hello world`。

我们仅仅用了 19 行代码就完成了一个单文件的 django 应用。其实它的原理很简单，就是把以前分开的代码给放在了一起，`urls.py`是 `tes.py` ,·`settings.py`是 `test.py` ，`views.py`是`test.py`，甚至连 `manage.py` 也是 `test.py` 。
这个小 demo 意义在于让大家了解 django 在运行的时候都发生了些什么，了解 django 的运行流程，为以后的开发打下基础。

## **REST 是什么**
### **先有个印象**
**REST**的种种好处我不再赘述。简单的说说为什么我们需要用 **REST** 。相信写过模板的同学都知道，只要哪怕页面中的数据有一丝丝变动，那整个页面都需要重新渲染，这对性能无疑是巨大的浪费，并且页面中只有一些元素会和数据相联系，比如列表中的 `<li>` 元素，如果数据有变化，能直接只更新 `<li>` 元素就好了，**REST** 就是为此而生。
提到 **REST** ，很多人可能知道一些概念，比如我们将要做的前后端分离的项目会用到它，大概明白它可以用用 **json** 来交换数据。**REST** 不是什么具体的软件或者代码，而是一种思想。这么说就太抽象了，**REST** 刚出来的时候是以论文的形式提出的，是一种设计的形式。对它的概念我们就先了解到这里。在本章，我们就把 **REST** 简单的当作是不再让 django 来渲染我们的前端，而是用 JS 在前端请求数据，用 JS 来渲染我们的页面。让  django 专注于后端的数据处理。
### **我们的 REST**
为了明确我们的 **REST** 开发，我们的前后端的分工大概如下：


```flow
st=>start: 客户端（浏览器）
fop=>operation: 前端页面
bop=>operation: 后端处理数据，并把数据以 json 形式发送到前端

st->fop->bop

```

我们的 **REST** 设计目前就是这样，实际上，**REST** 的抽象架构也就是这样的，

##**第一个REST项目**
这个项目的意义在于让大家了解 **REST** 的大致开发流程，踩踩需要踩的坑。这次我们会做一个简单的在线代码执行系统，由于不会用到数据库和模版，所以我们就使用刚才学习的单文件 django 来开发这个应用。

>注意，在开发这个应用时，需要你对 `JavaScript` 和 `JQuery` 有最基本的了解，要是你对他们还不了解，那就在敲代码时多多查阅文档，在练习当中学会他们。同时我们还会使用 `Bootstrap` 。在跟随教程敲代码时，注意多翻翻文档，一边敲一边查看文档，搞明白每一行代码是是什么意思。同时，代码注释也是很好的文档搜索关键词。

###**设计应用**
我们希望在用户访问我们的主页，并能在页面中编写python代码，在点击执行按钮时，主页上能返回程序执行的结果。

###**创建我们的应用**
新建一个文件夹，叫做 `online_python` ，并创建的目录结构：
<pre>
onlie_python/
    index.html
    online_app.py
</pre>

###**准备工作**
先把刚才在 `test.py` 里的代码复制过来，

`online_app.py`
```python
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls import url
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
```

我们需要用户在访问访问 `http://127.0.0.1:8000/` 时，视图应该返回主页的 html，也就是我们的 index.html 。由于我们并没有使用 django 的模板引擎，所以 `render` 函数也不能用了。所以我们需要自己手动的把 `index.html` 写入到响应中。所以把我们的 `home` 函数改成这个样子：

`online_app.py`

```python
def home(request):
    with open('index.html','rb') as f:
        html = f.read()
    return HttpResponse(html)
```
>注意，这里是以二进制读取的方式（`'rb'`）打开的 `index.html` ，也就是说最终的 `html` 的值为字节串，也就是 `b'....'`的形式，为什么要用二进制形式打开呢？
原因有两个：

>1. 最主要的也是最重要的，在一个 html 文件中，你不知道会有什么样的语言夹杂进去，一旦 python 无法识别其中的编码，就会报编码错误。然而实际上，读取并解析 html 是浏览器来完成的工作，django 只是简单的充当一个传递者的角色，它只需要把 html 文件传给浏览器即可。
2. 这也涉及到了一些浏览器和服务器数据传输的知识，浏览器与服务器的内容交互都是以二进制流的方式进行的，所以正规的响应就应返回字节串。django 的 `HttpResponse` 为我们做了转换的工作，所以你也可以把字符串传给 `HttpResponse`。




由于我们的 `index.html` 还没有任何内容，在 `index.html` 写入以下内容：

`index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>在线 Python 解释器</title>
</head>
<body>
<h1>在线 Python 解释器</h1>
</body>
</html>
```

在根路径下运行 `python online_app.py runserver` ，在浏览器中访问 `http://127.0.0.1:8000` ，你应该可以在浏览器中看到 在线 Python 解释器 的字样。

###**一切已经就绪，你准备好了吗？**
###**前端开发**
接下来，让我们专注于前端的开发，如果你对 js 和 jqery 不是很了解，那也没关系，教程中会进行讲解，如果有不懂的地方，利用教程中的关键词去查文档就行了。

我们需要使用 Bootstrap ，所以要引入 jqery。在 Bootstrap 的官网的[基本模板](http://v3.bootcss.com/getting-started/#template)给复制进来并替换掉原来的代码，删除其中的注释，此时你的 `index.html` 是这样的：

`index.html`
```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap 101 Template</title>
    <link href="css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>
    <h1>你好，世界！</h1>
    <script src="https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>
```
我们需要从页面中来引用 Bootstrap 的 js 文件和 css 文件，所以把第 8 行 替换为：
```html
<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
```

把第 13 行替换为：

```html
<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
```
现在，让我们正式开始前端页面的开发。最好把 Bootstrap 的官方文档打开，好方便随时查阅。

首先，我们需要对页面进行布局，先把我们页面的大概的样子设计好，我们的页面大概是这样的：
<pre>
+-------------------------+
+       ---标题----       +
+ 代码输入框   结果显示框 +
+            |            +
+  +------+  |  +------+  +
+  +      +  |  +      +  +
+  +      +  |  +      +  +
+  +      +  |  +      +  +
+  +------+  |  +------+  +
+            |            +
+                         +
+-------------------------+
</pre>

由于前端代码的特殊性，代码所在的行对最终的结果有影响，所以我给下面的代码手动添加了行号。
> ###**注意：在下面的代码中 + 与 - 分别代表代码的删除、增加，他们之前的数字是行号。**

把第 7 行的改成：
`index.html`
```html
7- <title>Bootstrap 101 Template</title>
7+ <title>在线 PYthony 解释器</title>
```
删除第 11 行内容， 并替换为Bootstrap 布局容器 `<div class=container></div>`，我们将会在这个布局容器中完成我们的页面。

`index.html`
```html
11- <h1>你好，世界！</h1>
11+  <div class="container"><!-- 页面的整体布局 -->
12+      
13+  </div>
```
我们可以大致把页面看成两个 Bootstrap container 的两个 row。
也就是：

<pre>
+-------------------------+
+       ---标题----       +---------> 标题单独为一行
+ 代码输入框   结果显示框   +------>+
+            |            +      +
+  +------+  |  +------+  +      +
+  +      +  |  +      +  +      +
+  +      +  |  +      +  +      +-----> 主体内容可以看作一行分成了两列
+  +      +  |  +      +  +      +
+  +------+  |  +------+  +      +
+            |            +      +
+                         +----->+
+-------------------------+
</pre>

按照上面的布局，我们这样来写代码：

`inxex.html`
```html
12+      <div class="row"> <!-- 这一行单独用来放标题 -->
13+        <div class="col-md-12"> <!-- 根据 bs规定，所有内容应放在 col 中。这一列占满一行 -->
14+           <p class="text-center h1"> <!-- text-center 类是 bs 中央排版，h1 是 bs 一号标题类 -->
15+           在线 Python 解释器
16+         </p>
17+        </div>
18+      </div>
19       <hr><!-- 标题和真正内容的分割线 -->
20+      <div class="row"></div><!-- 这一行用来放置主要内容 -->
```
保存你的代码，在浏览器中打开 `index.html` 你可以看到浏览器中央已经有个标题了。
![已经可以看见标题了](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/bootstrap-1.png)
接下来我们把代码输入框和结果显示框也完成。
因为我们的主体布局是左右布局，所以我们要先把左右布局先写好：

`index.html`
```html
20 <div class="row"><!-- 这一行用来放置主要内容 -->
21+  <div class="col-md-6"></div><!-- 代码输入部分 -->
22+  <div class="col-md-6"></div><!-- 结果显示部分 -->
23</div>
```
现在我们把需要在屏幕上显示的具体元素先写好：

代码输入部分：

`index.html`
```html
21<div class="col-lg-6"><!-- 代码输入部分 -->
22+  <p class="text-center h3">
23+    在下面输入代码
24+  </p>
25+  <textarea id="code" class="form-control" placeholder="Your code here."></textarea> 
26+  <button type="button" class="btn btn-primary">运行</button>
27</div>
```
结果显示部分：

`index.html`
```html
28<div class="col-lg-6"><!-- 结果显示部分 -->
29+   <p class="text-center">运行结果</p>
30+   <div class="col-lg-12"><textarea id="output" disabled placeholder="Please input your code and click <run> button to excute your python script" class="text-center form-control"></textarea></div>
31+   </div>
32</div>
```
我们为了不去处理前端复杂的转义符号，我们就用 `<textarea>` 来展示我们的文本，只是这个文本是不可编辑的。

我们大概的框架就已经写好了，目前，你的 `index.html` 应该是这个样子的：

`index.html`
```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>在线 Python 解释器</title>
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
  </head>
  <body><!--在下面的注释中 bs 代表 bootstrap -->
  <div class="container"><!-- 页面的整体布局 -->
      <div class="row"> <!-- 这一行单独用来放标题 -->
        <div class="col-lg-12"> <!-- 根据 bs规定，所有内容应放在 col 中。这一列占满一行 -->
          <p class="text-center h1"> <!-- text-center 是 bs 中央排版类，h1 是 bs 一号标题类 -->
            在线 Python 解释器
          </p>
        </div>
      </div>
      <hr><!-- 标题和真正内容的分割线 -->
      <div class="row"><!-- 这一行用来放置主要内容 -->
        <div class="col-lg-6"><!-- 代码输入部分 -->
          <p class="text-center h3">
            在下面输入代码
          </p>
          <textarea id="code" placeholder="Your code here." class="form-control"></textarea>
          <button id="run" type="button" class="btn btn-primary ">运行</button>
        </div>
        <div class="col-lg-6"><!-- 结果显示部分 -->
        <p class="text-center h3">运行结果</p>
        <div class="col-lg-12"><textarea id="output" disabled placeholder="Please input your code and click <run> button to excute your python script" class="text-center form-control"></textarea></div>
        </div>
      </div>
  </div>
    <script src="https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>
    <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
  </body>
</html>
``` 
现在，在浏览器里打开你的 `index.html` ，你会看到它是这个样子的：
![十分丑陋的界面](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/bootstrap-2.png)
现在我们已经看到了一个很粗糙的界面了，虽然很丑，但是一切都在按照我们的计划进行。
接下来，让我们来编写一些简单的 css 来让界面变的美观一点，你要是不知道这些 css 都是什么意思，MDN  是个查询文档的好地方。

在第8 行下面插入下面的代码：

`index.html`
```html
9+<style type="text/css">
10+    
11+</style>
```

按钮的位置好像太偏了，让我们用 css 来把它调整到一个合适的地方：

为了能够改变 button 的位置，我们需要在外面套上一个 `div` 元素，我们希望把按钮放在右边，所以需要用到 `text-right` 类
`index.html`
```html
29- <button id="run" type="button" class="btn btn-primary">运行</button>
29+ <div class="text-right"><button id="run" type="button" class="btn btn-primary ">运行</button></div>
```
然后为我们的 button 添加上 css 样式：

`index.html`
```html
10+#run {
21+    width: 20%; /*规定按钮的宽度*/
12+    margin-top: 10px; /*留出和输入框的间距*/
13+}
```

保存你的 `index.html` 文件，在浏览器中打开它，你会看到它是这个这样子的：
![美化之后的主页](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/bootstrap-3.png)

大家在打开的页面中，试着输入几行代码。你会发现这样的情况：
![不合适的输入框](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/bootstrap-4.png)
输入框的大小是固定的，只有手动的点击右边的翻页按钮才可以看到下面的代码，这样的输入框用起来简直不方便，我们需要改善一下用户体验。我们想让输入框的大小随着输入代码的行数而改变，也就是说，输入框的大小是动态变化的，同时，我们希望我们的输出框也是动态变化的。这就需要用到 js 了。
在 41 行下面插入一个 `<script>` 标签
`index.html`
```html
42+<script>
43+    
44+</script>
```
我们先来梳理一下动态输入输出框的逻辑。输入一次大小就变化一次，也就是说，它们的 css 是动态变化的，也就是它们的高度是动态变化的。在 `<textarea>` 中，当用户的输入超出了 `<textarea>` 的大小时，它的右边就会自动出现一个滚动条，如果我们让 `textarea` 的高度等度滚动条的高度，那么此时 `<textarea>` 的高度就等于用户输入的文本高度了。所以我们需要在用户输入一次之后就调整一下大小。
先来编写改变大小的函数:

`index.html`
```html
43+ // 改变大小函数
44+function changeSize(ele){
45+   $(ele).css({'height':'auto','overflow-y':'hidden'}).height(ele.scrollHeight)
46+}
```
我们用 js 动态的改变了 `<textarea>` 的高度 ，在这里我们需要注意一点，我们并没有一来就把高度设置为 `<textarea>` 滚动条的高度，而是先让它自动适应，然后再改变它的大小。这是为了让输入框能够自动“缩回去”，想想看，如果我输入了几行文本，出现了滚动条，此时我们的输入框自动调整大小，滚动条消失，然后又删除这几行文本，你会发现，我们的输入框“回不去”了，为什么呢？因为此时，滚动条的高度还是原来的高度，所以输入框还是原来的大小，需要改变这个大小，所以我们就需要 `height:auto` 来帮我们“缩回去。

>没看懂刚才的解释？没关系，等我们完成这一部分，会有一个小实验，大家跟着试一次就明白了。

现在把这个动态的变化应用到输入框。

`index.html`
```html
47+// 应用到输入框
48+$('#code').each(function(){
49+    this.oninput = function(){
50+      changeSize(this)
51+    }
52+  })
```
现在，保存你的 `index.html`，在浏览器里打开他，不出意外的话，你看到的会是这个效果：
![动态输入框效果](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/bootstrap-5.gif)
现在我们来做之前说的实验。
大家把 45 行改成这样，去掉了：

`index.html`
```html
45- $(ele).css({'height':'auto','overflow-y':'hidden'}).height(ele.scrollHeight)}
45+$(ele).css({'height':ele.scrollHeight,'overflow-y':'hidden'})
      }
```
保存之后在浏览器里打开，你会发现效果是这样的：
![不能“缩回去”的输入框](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/bootstrap-6.gif)

所以我们先使 `height:auto` ，再让高度等于滚动条的高度，才能让输入框“缩回去”。现在实验做完了，把 45 行改回去。

`index.html`
```html
45-$(ele).css({'height':ele.scrollHeight,'overflow-y':'hidden'})}
45+ $(ele).css({'height':'auto','overflow-y':'hidden'}).height(ele.scrollHeight)}
```
仔细的读者也许已经发现，输入和输出框右下角有个小三角，那是浏览器为了方便用户自己调整大小而产生的，然而我们并不希望用户这样做，所以我们需要禁用这个功能，只需要在 css 里加入 `resize: none;` 就可以了。是不是觉得字体很小？我们也把字体改的大一点。

`index.html`
```html
14+#code {
15+  font-size: 25px;
16+  resize: none;
17+}
18+#output {
19+  font-size: 25px;
20+  resize: none;
21+}
```
此时你的 `index.html` 应该长得像这样：

`index.html`
```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>在线 Python 解释器</title>
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <style>
      #run {
          width: 20%; /*规定按钮的宽度*/
          margin-top: 10px; /*留出和输入框的间距*/
      }
      #code {
        font-size: 25px;
        resize: none;
      }
      #output {
        font-size: 25px;
        resize: none;
      }
    </style>
  </head>
  <body><!--在下面的注释中 bs 代表 bootstrap -->
  <div class="container"><!-- 页面的整体布局 -->
      <div class="row"> <!-- 这一行单独用来放标题 -->
        <div class="col-lg-12"> <!-- 根据 bs规定，所有内容应放在 col 中。这一列占满一行 -->
          <p class="text-center h1"> <!-- text-center 是 bs 中央排版类，h1 是 bs 一号标题类 -->
            在线 Python 解释器
          </p>
        </div>
      </div>
      <hr><!-- 标题和真正内容的分割线 -->
      <div class="row"><!-- 这一行用来放置主要内容 -->
        <div class="col-lg-6"><!-- 代码输入部分 -->
          <p class="text-center h3">
            在下面输入代码
          </p>
          <textarea id="code" placeholder="Your code here." class="form-control" ></textarea>
          <div class='text-right'><button id="run" type="button" class="btn btn-primary ">运行</button></div>
        </div>
        <div class="col-lg-6"><!-- 结果显示部分 -->
        <p class="text-center h3">运行结果</p>
        <div class="col-lg-12"><textarea id="output" disabled placeholder="Please input your code and click <run> button to excute your python script" class="text-center form-control"></textarea></div>
        </div>
      </div>
  </div>
    <script src="https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>
    <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
    <script>
      // 动态大小函数
      function changeSize(ele){
        $(ele).css({'height':'auto','overflow-y':'hidden'}).height(ele.scrollHeight)
      }
      // 应用到输入框
      $('#code').each(function(){
          this.oninput = function(){
            changeSize(this)
          }
        })
    </script>
  </body>
</html>
```
保存你的 `index.html` ，在浏览器里打开它，你看到的应该是这样：
![最终的样子](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/bootstrap-7.png)

到目前，我们有关界面 UI 显示的的部分已经全部完成了。当然，有兴趣的同学可以自己加一个背景。我自己随便选了个背景。。
![我加的背景](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/bootstrap-8.png)

现在重头来了，我们将实现前端页面和后端的交互部分。
同样的，我们先来完成对交互的设计。我们希望这样来交互：
用户点击 `运行` 按钮时，js 自动发送输入框的代码，待后端处理完之后，接收来自后端的结果，然后再把结果显示在输出框内。我们希望我们用 `POST` 方法向后端的 `/api/` 路径发送用户代码。

在真正开始开发之前，在这里我们会用到一个东西，叫做 `ajax`，它相当于前端的 `requests` ，为我们提供了 js 向 URL 发送请求的功能，只是功能没 `requests` 那么强大，jquery 提供了 ajax 支持，所以我们直接使用就好了。不过我建议，对 ajax 不了解的的同学，现在最好打开 jquery 的 ajax 部分的文档，在跟随代码时对照着看。

先获取用户输入框代码:

`index.html`
```javascript
61+//获取输入框代码
62+function getCode(){
63+  return $('#code').val()
64+}
```

将获取的结果打印到输出框，同时，输出框需要根据内容的大小而改变。
`index.hthml`
```javascript
65+//打印结果到输出框并改变输出框大小
66+function print(data){
67+  var ele = document.getElementById('output')
68+  output.value = data['output']
69+  changeSize(output)
70+}
```
需要注意的是，我们的打印函数最终是作为 ajax 请求成功之后的回调函数来使用的，ajax 会自动往里面传入一个 data 参数，这个 data 是响应数据。我们并没有直接就打印 data ，因为万一后端需要对数据做进一步的分类，比如多一个 status 字段来表示代码执行状态（成功或者失败），那么直接打印 data 就是不合适的做法了。所以我们选择的是提取 data 的 `output` 字段，这样不管 data 怎么变，只要有 `output` 参数，我们展示结果的代码就能正常执行。

最后，把发送代码的动作绑定到点击按钮：

`index.html`
```javascript
71+// 点击按钮发送代码
72+$('#run').click(function(){
73+  $.ajax({
74+    url:'/api/', //代码发送的地址
75+    type:'POST', // 请求类型
76+    data: {'code':getCode()},//调用代码获取函数，获得代码文本
77+    dataType: 'json', //期望获取的响应类型为 json
78+    success: print // 在请求成功之后调用 pprint 函数，将结果打印到输出框
79+  })
80+})
```
到这里，我们前端的所有内容就算完成了。完整的前端代码大家可以在 [github](https://github.com/Ucag/django-rest) 中找到，就不贴在这里了。接下来，让我们进入后端开发。

###后端开发
经过了漫长的前端开发，我们终于来到了后端。我们的代码在这里将不会再标行数。所以大家可以灵活安排自己的代码，自由的做相应的调整。

打开 `online_app.py` ，现在顶部引入：

`online_app.py`
```python
from django.views.decorators.http import require_POST # 目前的 API 视图只能用于接收 POST 请求
from django.http import JsonResponse # 用于返回 JSON 数据
```

先来编写我们的 api 视图函数：

`online_app.py`
```python
@require_POST
def api(request):
    code = request.POST.get('code')
    output = run_code(code)
    return JsonResponse(data={'output':output})
```
具体运行代码的函数我们将会在下面实现。在下面把我们的 URL 配置改成这样，加上我们的 api 视图。

`online_app.py`
```python
urlpatterns = [url('^api/$',api,name='api'),
                url('^$',home,name='home')]
```

现在我们来实现 `run_code` 函数。在接着往下看之前，先做个深呼吸，因为这个函数会用到你可能不熟悉的模块 `subprocess` ，当很多人看到这个模块的名字或者听到“多进程”这个词的时候，或许他能对 python 实现多进程的种种缺点批判一番，但是当叫他真的写个多进程时却会感到十分为难。别担心，我们只是在这里简单的使用 `subprocess` 封装好了的功能。为了更好的编写这个函数，确保它的功能正常，我们需要为这个函数编写测试。所以我们需要在编写好了这个函数在把它应用到我们的 app 中，所以在你的 app 的路径，也就是 `online_python` 下建一个新文件 `test.py` 。为了一切从简，这里我们就不使用 `unittest` 了，我们使用人肉测试。

先引入 `subprocess`
`test.py`
```python
import subprocess
```

接下来我们需要仔细考虑 `run_code` 会遇到的情况：

1. 能够正确执行来自客户端的代码。也就是说，如果客户端的代码是正确的，那么 `run_code` 的输出结果也应该是预期的那样。
2. 当用户代码发生错误时，能够返回错误信息。来自客户端的代码难免会有错误，我们需要像 python 解释器一样返回详尽的错误跟踪信息。
3. 当用户的代码执行时间过长时，自动中断代码的执行，并在前端给出执行超时提示。有的时候，客户端的代码可能陷入死循环，为了提早让用户知道代码异常，我们应该主动中断代码执行。有的时候用户代码可能是正确的，但是执行时间真的太长，我们也需要中断执行，不能让这个进程一直占用系统资源。一旦用户过多，系统资源很快就会支撑不住

在编写 `run_code` 的过程中，也是对 `subprocess` 模块的学习，所以大家可以把 [subprocess 文档打开对照着看](https://docs.python.org/3.5/library/subprocess.html) 。

首先，`run_code` 能正确的执行客户端代码。由于我们是直接运行的字符串，所以首先得解决如何用 python 脚本来执行 python 字符串。那就是使用 `python -c <your_script_code>` 命令。所以我们应该开一个进程来执行这个命令。在 `subprocess` 中，执行一个进程最常用的方法是 `subprocess.run(*args,**kwargs)`， 但是它不返回输出结果，所以我们需要使用 `subprocess.check_output(*args,**kwargs)`。现在我们来编写 `run_cdoe` 函数：

`test.py`
```python
import subprocess

def run_cdoe(code):
    output = subprocess.check_output(['python','-c',code])
    return output

code = """print('Test success')"""
print(run_cdoe(code))
```
现在我们来看看输出，看看是不是我们想要的输出：
![输出](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/test-1.png)
输出的是字节串。但是我们期望的是字符串。我们有两种办法，第一种是直接手动转换结果，将 `output` 转换为 `string`，但是这会有个问题。你要是直接解码，会出现一个问题，如果你得到的结果是来自你的 shell ，那输出结果的编码就是 shell 的编码，每个系统的 shell 编码是不同的，难道需要我们为每个 shell 编写解码代码吗？所以这个看起来可行的方法是没有普适性的。所以我们就只能采用第二种方法了，第二个方法很简单，那就是加上 `universal_newlines=True` 参数，加上这个参数之后，`subprocess` 会自动为我们将输出解码为字符串。它具体是怎么实现的，大家可以去文档看介绍。现在正确执行代码给出正确输出结果的功能解决了。
![期望输出](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/test-3.png)

现在解决第 2 个需求。输出错误。
在 subprocess 中，有个参数是 `stderr` ，大家看意思就已经明白它是干什么的了，是用来控制错误输出流的。默认的错误输出是输出到主进程的，也就是调用这个进程的进程。让我们来故意引发一个错误，看看具体是怎么回事：
[错误输出](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/test-2.png)
大家可以看到，子进程的错误输出也在主进程的错误输出里。
我们希望错误输出也能输出到 `output` 上，`output` 本来是子进程的标准输出，所以现在我们需要捕捉子进程的错误输出流导。怎么做呢，那就是让 `stderr=subprocess.STDOUT`，大家就会看到这个效果：
![错误输出流重定向](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/test-4.png)
子进程的报错已经看不到了，因为错误输出流已经被重定向到了子进程。但是我们看，主进程依然报错了。这是 `sbuprocess` 的机制，在子进程没有执行成功时，就会引发 `subprocess.CalledProcessError` ，这个错误的 `output` 属性包含了子进程的错误输出。所以我们这样来编写 `run_code`：

`test.py`
```python
import subprocess

def run_cdoe(code):
    try:
        output = subprocess.check_output(['python','-c',code],universal_newlines=True,stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
    return output
```

我们来看看效果：
![最终效果](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/test-5.png)
现在还剩下第 3 个需求，控制客户端代码执行时间。同样的我们还是依靠给 `subprocess` 传递参数来实现控制，这个参数就是 `timeout` ，它的单位是秒，所以我们希望在 30 秒之后还没执行结束就中断执行。在 `subprocess` 中，超时引发的错误是 `subprocess.TimeoutExpired`，它的 `output` 参数也包含了子进程的错误输出。所以把 `run_code` 改成这样：

`test.py`
```python
import subprocess

def run_cdoe(code):
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
```
让我们来看看测试：
![最终测试](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/test-6.png)
效果不错！大功告成！
现在把我们的 `run_code` 函数复制到 `online_app.py` 里，记得也要导入 `subprocess` 库。
最终你的 `online_app.py` 会是这样的：

`online_app.py`
```python
from django.conf import settings
from django.http import HttpResponse, JsonResponse# JsonResponse 用于返回 JSON 数据
from django.conf.urls import url
from django.views.decorators.http import require_POST
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
```
我们的“人肉测试模块”已经完成它的任务，现在可以删掉了。现在我们完成了前后端的功能开发，让我们来试试吧！在根路径运行 `python online_python.py runserver`，访问 `http://127.0.0.1:8000` 。试试往里面输入代码，看看能不能得到想要的结果。然后你会发现输出框什么变化也没有！打开控制台看看，你会发现这个情况：
![又出问题了！](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/test-7.png)
请求被禁止了，你可以在 django 的控制台kan原来是跨域请求错误。跨域请求 django 是怎么处理的呢？写过模板表单的同学都知道，是通过给表单加 `{% csrf_tokne %}` 来实现的。那现在我们已经是 REST 架构了，已经不需要它了，那有的同学又会问了，那我们怎么防止跨站脚本攻击呢？那就是靠 JWT token，但是这一次我们不实现 JWT token。所以我们就选择禁用 csrf 功能。所以修改 `onlime_app.py` 如下：

现在顶部引入：
`online_app.py`
```python
from django.views.decorators.csrf import csrf_exempt
```
把我们的 api 视图修改为:
`online_app.py`
```python
@csrf_exempt
@require_POST
def api(request):
    code = request.POST.get('code')
    output = run_code(code)
    return JsonResponse(data={'output':output})
```
现在赶紧运行 `python online_app.py runserver` ，访问 `http://127.0.0.1:8000`，写几行代码试试，运行一下。
![最终效果](https://raw.githubusercontent.com/Ucag/django-rest/master/Chapter-one/img/final.png)
恭喜你完成了第一个 REST APP! 
##下一章做什么？

在本章，我们知道了单个文件的 django 也可以运行，通过单文件的 django 我们大致了解了 django 初始化运行流程是什么，同时我们简单的了解了 REST 的概念，并构建了一个简单的 APP 。在下一章，我们将会深入 REST ，我们将会制作一个符合 REST 标准的 APP ，以此来熟悉 REST 标准，同时了解 REST 最核心的概念————一切皆资源。











