#Django RESTful 系列教程（三）（中）
---
在上一节中我们了解了 DRF ，现在我们要开始学习 Vue 了，这一前端神器。同样的，这不是官方文档复读机，我们会讲一些官方文档没有讲的东西，如果你对本节中所涉及到的东西想有更深的了解， [vue 官方文档](https://cn.vuejs.org/)是个好去处。一个好消息是，Vue 与 Django 的原理有着相通之处，大家应该可以很轻松的掌握，只是有一些小的知识点细节需要明确。同时 js 和 py 都支持面向对象编程，所以大家在看教程时，着重联系面向对象的编程思维，如果 js 代码不理解，那就想想同样的 python 代码是怎么写的。

本章会涵盖以下知识点：

1. Vue 原理。
2. 认识组件。
3. Vue 特色语法。

>Vue 的中文文档已经非常优秀，作为国人开发的框架，对国人是非常友好的，并且官方文档的入门教程是真的不错，强烈建议大家去看看。

##Vue 原理
对于 Vue ，很多人应该听说过 [MVVM ](https://en.wikipedia.org/wiki/Model_View_ViewModel)模型，但是同 MTV 一样，很少有人能清楚的解释这到底是怎么回事。

![MVVM 模型](https://images.contentful.com/emmiduwd41v7/7zcSy3ZHmEGI0cykSa6eKy/2a6efbc6ceb05cc0484bcf6b403b7b3c/Image2.JPG)

图片来源：https://academy.realm.io/cn/posts/mobilization-lukasz-mroz-mvvm-coordinators-rxswift/

View: 展示数据的部分，也就是我们可以在页面上看到的 UI 。 View 使用 ViewModel 来做出对应的状态改变。同时，View 不会也不能进行改变数据的操作，它是通过 ViewModel 来修改数据的。也就是说，这里的 View 就真的只是个 View ，就像是被渲染之后的模板一样，就是一个 html 文件，什么数据操作都不能做。

ViewModel: 数据的业务逻辑部分。所有的业务逻辑都在这里。不仅包含数据的处理逻辑，还包括 View 的逻辑都在这里了，所以叫做 ViewModel 。比如我们之前写的 `code-options` 的部分，不同的数据对应不同的 View 状态。这和 Djanogo 的模板很相似，我们在模板中编写了 html 相应的逻辑，最后由模板引擎渲染成固定的 html 文档。大家可以把这部分理解为前端的模板引擎，不仅包含视图逻辑，还包含对后端的数据处理。

Model: 储存数据的地方。也就是我们的 Store 了，它负责向后端 API 发起请求，储存收到的数据。

我们来看看这样一个 MVVM 流程是怎样走完的：

1. 用户看到了一个按钮（View），点击了它（View 发出信号，ViewModel 捕捉信号）。
2. ViewModel 收到信号，根据 View 逻辑，此时应该从 Store 中获取数据，数据在处理之后，数据传到 View 中。
3. Store 收到请求，发现现在不需要重新请求数据，就直接把数据给了发起请求的 ViewModel 。

所以，总结一下，MVVM 的唯一不同之处就是把视图逻辑和数据逻辑放在了一起，称为“ViewModel”，View 的逻辑也被看成了是数据的一部分。剩下的部分和 Django 其实差不多。

##认识组件
在开始之前，我们需要做一些准备工作。建立如下文件结构：

```
vue_learn/
    vue.js
    index.js
    bootstrap.js
    jquery.js
    bootstrap.css
    index.html
```

vue.js： vue 的源文件，可以直接从[这里](https://vuejs.org/js/vue.js)复制粘贴，也可以直接从我的 github 仓库中拉取。
index.js: 空文件，我们将会在这里学习 vue 。
bootstrap.js： bootstrap 的 js 文件。可以从上一章的项目中复制。
bootstrap.css: bootstrap 的 css 文件。可以从上一章的项目中复制。
jquery.js: bootstrap.js 的依赖，必须使用。可以从上一章的项目中复制。
在 index.html 中写入下列代码：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Vue-learn</title>
    <link rel="stylesheet" type="text/css" href="bootstrap.css">
</head>
<body>
<div id="app"></div>
<script src="jquery.js"></script>
<script src="bootstrap.js"></script>
<script src="vue.js"></script>
<script src="index.js"></script>
</body>
</html>
```

准备工作做完了。编辑器中打开你的 index.js 和 index.html，同时用浏览器打开 index.html ，以便我们随时查看编写的效果。这里需要你调整好自己的窗口规划，最好能够使用多任务桌面，如果你使用的 win7 ，`Dexport` 是个支持这项功能的好软件，支持快捷键切换桌面，特别方便，并且还是免费的。

###组件

####组件是什么？
正如我们在第一章中编写 html 一样，先把页面的框架搭好，再往每个部分里填 UI ，这些 UI 便被称为组件了。我们的 code-list 是一个组件，code-options 按钮组也是组件，我们在需要的时候渲染它们。就像是搭积木一样，组件是积木，网页就是我们用不同的积木搭建起来的堡垒。

把眼光放的再开一点看，我们的框架结构本身，也是个组件。只是这些组件没有形状，只有结构，等待其它组件被填充进去。在页面中，一切皆可为组件，相信大家在了解 REST 一切及资源之后理解这个应该不难。

所以，在我们之前写的前端代码中，那些包含模板字符串的函数就是我们组件了，我们可以随时调用他们来搭建页面。

####组件是实例。
因为我们使用的是 Vue ，所以应该使用 Vue 来构建我们组件。我们在 python 知道类和实例的概念，在这里我们说的实例也就是 Vue 类的实例。所以，象这样写我们就有了一个 Vue 实例：

```javascript
let vueInstance = new Vue({...}) //{...} 为选项对象
```

既然是实例，那么 Vue 类有的属性和方法，Vue 实例也就是组件也应该有这些方法。同时，他们的参数，也就是选项对象也应该相同。然而事实是，有少数几个选项只在运行 `new` 时有效。至于为什么这样做，在下面会提到，

刚才我们也提到，组件之间可以相互组合，共同构成一个“大组件”，也就是我们的网页。那怎么把 Vue 和页面中的 html 相联系起来呢？

如果我们想要使用一个组件，我们需要告诉 Vue 我们需要把这个组件放在哪里。有几种方式可以选择，我们一个一个来看看。

第一种，**只**使用 `el` 选项。仅仅在 `new` 时有效。

`index.html`
```html
<div id="app">
    {{ message }}
</div>
```
`index.js`
```javascript
let cp = new Vue({
    el: '#app',
    data:function(){
        return {
            message:'Hello Vue!'
        }
    }
})
```
保存他们并刷新你的浏览器，你会看到在 html 中本来的 `{{ message }}`部分被替换为了 `Hello Vue!` 。

我们使用 `el` 选项，告诉 Vue 我们要把匹配 `#app` 的 html 元素作为组件。把一个元素作为组件，也就是相当于告诉 Vue 我们的组件要放在这里了。

看到 `{{ }}` 我相信大家一定都非常熟悉了，这不就是模板的语法吗？那选项中的 `data` 参数是做什么用的呢？正如它的名字一样，这是给组件提供数据的地方。为什么使用的是函数来返回数据而不是直接把 `data` 定义为一个对象呢？保持你的好奇心。这个问题我们之后再来解答，现在你可以简单的就像理解我们在前端管理 API 时所做的那样，为了方便变动数据。

第二种方式，使用 `template` **和** `el` 选项。

`index.html`
```html
<div id="app">
    {{ message }}
</div>
<div id="app2"></div>
```
`index.js`
```javascript
let cp2 = new Vue({
    el:'#app2',
    template:`
    <h1>{{ message }}</h1>`,
    data:function(){
        return {
            message: 'Hello Component 2!'
        }
    }
})
```
保存他们并刷新你的浏览器，你会看到在 html 中，本来的 `<div id="app2"></div>` ,被替换为了 `<h1>Hello Component 2!</h1>` 。

我们可以把本来的组件写在 `template` 选项中，使用 `el` 选项告诉 Vue 我们会在哪里放这个组件，Vue 会用 `template` 的内容**替换**被匹配到的元素。替换，也是一种告诉 Vue 我们要把组件放到哪儿的方法。需要注意的是，`template` 只能有一个外层标签，因为有多个的话 Vue 就不知道该把哪个元素替换到目标标签上去。 

第三种，使用 `$mount` **和** `template`。

`index.html`
```html
<div id="app2"></div>
<div id="app3"></div>
```
`index.js`
```javascript
let cp3 = new Vue({
    template: `<h1>{{ message }}</h1>`,
    data: function(){
        return {
            message:'Hello Component 3!'
        }
    }
})
cp3.$mount('#app3')
```
保存他们并刷新你的浏览器，你会看到在 html 中，本来的 `<div id="app3"></div>` ,被替换为了 `<h1>Hello Component 3!</h1>` 。

当没有使用 `el` 指定要把一个组件放在哪里时，这个组件处于“**未挂载**”状态。我们可以在创建一个组件之后，使用其 `.$mount` 方法，将它“**挂载**”到一个元素上，这个元素会被 `template` **替换** 掉。

####组合组件
正如我们刚才所说，组件是可以被“组合”的。按照刚才的写法，我们应该怎样将组件们结合起来呢？也就是说，我们怎样做才能让组件知道有其它的组件存在呢？

`index.html`
```html
<div id="app5"></div>
```

`index.js`
```javascript
let cp4 = {
    template:'<h1>{{ message }}</h1>',
    data:function(){
        return {
            message: 'Hello Component 4!'
        }
    }
}
let cp5 = new Vue({
    el:'#app5',
    template:`
    <div class="text-center">
    <cp-4></cp-4>
    {{ msg }}
    </div>`,
    components:{
        'cp-4':cp4
    },
    data:function(){
        return {
            msg:"I'm Component 5!"
        }
    }
})
```
保存他们并刷新你的浏览器，你会看到我们的组件成功的被组合在了一起，可以查看一下浏览器，看看他们是否都在同一个`div`下。

组合组件的方法就是使用 `components` 选项，我们不需要传给 `components` Vue 实例，只需要传子组件的名字作为属性，它的选项作为值就好了。以上的过程，我们称为“**注册组件**”这样，组件就可以使用在 `components` 中的其它组件了。并且，只需要像使用普通的 html 一样就可以使用它了。

刚才说的是“**局部注册**”，也就是只是把组件和某个特定的组件组合起来。但是有时候，我们希望能够“**全局注册**”这个组件，也就是说，我们希望能够在所有的组件中使用它。 Vue 为我们提供了全局注册的方法。

`index.html`
```html
<div id="app5"></div>
<div id="app6"></div>
<div id="app7"></div>
```
`index.js`
```javascript
Vue.component('global-cp',{
    template:`<h1>{{ msg }}</h1>`,
    data:function(){
        return {
            msg:"I'm global!"
        }
    }
})
let cp6 = new Vue({
    el:'#app6',
    template:`<div>
    I'm app6!
    <global-cp></global-cp>
    </div>`
})
let cp7 = new Vue({
    el:'#app7',
    template:`<div>
    <global-cp></global-cp>
    {{ msg }}
    </div>`,
    data:function(){
        return {
            msg:"I'm app7!"
        }
    }
})
```

保存他们并刷新你的浏览器，你会看到我们的全局组件已经起作用了。我们使用的是 Vue 类的方法来添加全局组件。类的就是实例的，所以类有了某个组件，那么用这个类生成的实例也应该有这些组件。

####正确的使用组件
刚才我们说道，一个网页也可以是一个组件。也就是说，我们可以先创建一个空的组件，然后让这个组件来容纳其它的组件，这样我们就可以实现仅仅使用 Vue 就可以对网页进行全权的控制，从而实现许多酷炫的功能。SPA（Single Page Application，单页应用）就是一个很好的范例。整个应用只有一个网址，网页的所有变动都是组件的变动，同时，这也减轻了前端的压力，不用再去写那么多页面，只需要写变化的组件就行了。

所以，组件的一般写法是：
    1. 先写一个空的组件作为组件入口。
    2. 通过在这个空的组件中组合其它组件来达到组合成网页的目的
    
删除 `index.html` 中所有的 `div` 元素，删除 `index.js` 中的所有代码，编写代码如下：

`index.html`
```html
<div id="app"></div>
```
`index.js`
```javascript
let navBar = {
    template:`
    <nav class="navbar navbar-default">
        <div class="container-fluid">
              <ul class="nav navbar-nav">
                <li class="active"><a href="{{ home }}">Home</a></li>
                <li><a href="{{ about }}">About</a></li>
              </ul>
        </div>
    </nav>
    `,
    data:function(){
        return {
            home:'http://example.com/',
            about:'http://example.com/about'
        }
    }
}

let mainContent = {
    template:`
    <h1>{{ content }}</h1>
    `,
    data:function(){
        return {
            content:'This is main content!'
        }
    }
}
let app = {
    template:`
    <div class="container">
        <div class="row">
        <nav-bar></nav-bar>
        </div>
        <div class="row">
        <main-content></main-content>
        </div>
    </div>`,
    components:{
        'nav-bar':navBar,
        'main-content':mainContent
    }
}

let root = new Vue({
    el:'#app',
    template:`<app></app>`,
    components:{
        'app':app
    }
})
```
保存他们并刷新你的浏览器，你看到的会是这样：
![正确使用组件.png]() 

我们仅仅调用了一次 `new Vue()` ，把 `root` 作为根组件。组件 `root` 基本上是组件 `app` 构成的，为什么不直接把 `app` 的逻辑放入 `root` 中呢？因为我们的 `app` 可能不止一个，可能随时会被替换成其它的 `app` 组件，比如我们的网页有两套布局模式，一套为移动端布局，一套为PC端布局，我们可能会根据需求来更换布局，要是直接写死在根组件里，会十分的不便。

关于组件，我们就暂时学到这里。在最后一节，我们将会学习更多关于组件的知识。

###Vue 组件特色语法。
有许多的特殊语法可以在组件中使用，帮助我们提高开发的效率。如同模板一样，它们都有自己的语法。

####准备工作
在 `vue_learn` 下新建一个 html 文档，名为 `grammer.html`，编写如下代码：

`grammer.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Grammer</title>
</head>
<body>
<div id="app"></div>
<script src="vue.js"></script>
<script type="text/javascript">
    
</script>
</body>
</html>
```
我们接下来的大部分工作都将会在空的 `script` 标签中完成。

####`{{ }}`
#####data
在 Django 模板中，`{{ }}` 中是用来写变量的，在渲染时，变量会被替换为相应的变量值。 在 Vue 中，`{{ }}` 也做了同样的事情，但不一样的是，这个变量值是动态的，也就是“响应式”的。

`grammer.html`
```html
<script type="text/javascript">
    let app = new Vue({
        el:'#app',
        template:'<h1>{{ msg }}</h1>',
        data: function(){
            return {
                msg:'Grammer'
            }
        }
    })
    setInterval(function(){
        if (app.msg=='Grammer'){
            app.msg = 'Vue'
        } else {
            app.msg = 'Grammer'
        }
    }, 500)
</script>
```

保存并在浏览器中打开，你会看到这个效果 ![响应式的数据变化]()。

仔细观察我们代码，我们发现：

1. 我们并没有直接使用 `app.data.msg` 来改变数据，而是使用 `app.msg` 来改变 `msg` 属性的值。
2. 虽然我们是在实例化组件之后才改变的 `msg` 属性值，但是数据变化在 UI 上依然被表现出来了。

对于第一条，反应快的同学已经发现了，我们传给 Vue 的是它的选项对象，选项对象又不一定是作为 Vue 实例属性来使用的。事实上，如果想要访问实例的原始 `data` 对象，应该使用实例的 `$data` 属性。但是，我们 `data` 选项返回的**数据对象**却成了 Vue 实例的属性。所谓数据对象，就是一个纯粹的 **key/value** 对，和我们的 python 字典一样。Vue 官方也建议，数据对象最好只有纯粹的键值对，因为数据对象的原型链将会不会起作用。

为什么 `data` 返回的数据对象会成为 Vue 实例的属性呢？因为 Vue 在生成组件实例时，会把 `data` 返回的数据对象递归的设置为组件实例的 `getter/setter` 。 或许这里的 `getter/setter` 不怎么好理解，它的原理其实和 python 的描述符类似。`getter` 如同 `__get__` 方法，拦截了读取数据的操作，`setter` 如同 `__set__` ，拦截了赋值操作。当有任何的数据变动时，Vue 实例的 `setter` 在完成赋值操作之后，还会告诉另外一个负责绘制 UI 的方法“该修改 UI 上的数据啦”，这样就实现了动态的“响应式”操作，当然，真正的响应式原理还需要考虑到更多的东西。

既然我们知道了数据对象会被设置为实例的属性，所以我们完全可以在编写组件时直接使用 `this` 来访问组件属性。

回到 `{{ }}` ，当 Vue 遇到 `{{ }}` 时，它会在组件的数据对象中寻找对应的属性值。所以，如果想要在 `{{ }}` 中使用某个变量，需要**先**在数据对象中定义它，不然就会出错。

#####computed
`computed` 是选项对象的属性之一，我们可以使用这个选项对数据做一些复杂的处理。删除 `grammer.html` 中我们编写组件的 `script` 标签代码。重新编写如下：

`grammer.html`
```html
<script type="text/javascript">
    let app = new Vue({
        el:'#app',
        template:'<p>Hello, {{ name }}. {{ greeting }}</p>',
        data: function(){
            return {
                name:'Ucag'
            }
        },
        computed:{
            greeting: function(){
                return 'I am Vue' + 'Nice to meet you ' + this.name
            }
        }
    })
</script>
```
保存并在浏览器中打开，你会看到浏览器输出了 `Hello, Ucag. I am Vue Nice to meet you Ucag` 。`computed` 中的数据成功的被 `{{ }}` 语法获取。

`computed` 选项中的键被成为“计算属性”，Vue 会把这些属性绑定到组件中，也就是说，我们同样也可以用 `this` 来访问他们。 那它和 `data` 选项的差别在哪里呢？

1. `computed` 中的计算结果会被缓存。通过例子，我们可以看出，`computed` 的每个属性值需要是一个函数。这个函数的返回值会被缓存。这个特性是很有用的，比如我们可以把对 API 的请求写在这里，当在使用组件时，可以放心的调用计算属性，而不用担心多余和不必要的请求。通过 2 的例子更能说明计算属性的缓存特点。
2. 更新触发机制不同。数据对象，也就是 `data` 的返回的对象被更新之后，UI 会同时更新。但是对于计算属性就不会触发更新，也就是说属性不会重新计算，得到的值还是原来的计算值。

要是此时你在浏览器的控制台输入：
```
>app.greeting = 'Good morning'
<: 'Good moring'
>app.gretting
<: "I am Vue Nice to meet you Ucag"
```
我们可以看到，`gretting` 的值还是原来缓存的值。那么如何才能触发计算属性的更新呢？只有在计算属性依赖的数据对象的属性改变的时候才会触发更新。

```
>app.name = 'Ace'
<: 'Ace'
>app.greeting
<: "I am Vue Nice to meet you Ace"
```
我们可以看到计算属性已经重新计算了。

所以，如何合理使用计算属性呢？当你遇到下列情况的时候应该使用计算属性：

1. 数据要经过复杂的处理。我们可以把复杂的数据处理步骤放在这里，在一次处理之后结果就会被缓存。
2. 不希望主动的响应式变化。我们可以看到，计算属性是“被动响应”的，只有在依赖的数据对象属性改变之后才会重新计算。

既然被称为计算属性，`computed` 提供的数据处理功能不局限于简单的调用属性对应的函数。虽然那计算属性的触发是取决于数据对象，但是我们依然可以让计算属性在被直接改变时做一些事情。我们还可以对属性设置 `getter` 和 `setter`。重新编写 `app` 组件如下：

`grammer.html` 
```javascript
    let app = new Vue({
        el:'#app',
        template:'<p>Hello, {{ name }}. {{ greeting }}</p>',
        data: function(){
            return {
                name:'Ucag'
            }
        },
        computed:{
            greeting: {
                get: function(){
                    return 'I am Vue. ' + 'Nice to meet you ' + this.name
                },
                set: function(value){
                    console.log('You can not change greeting to ' + value)
                }
            }
        }
    })
```
保存并在浏览器中打开，打开你的浏览器控制台，输入下面的代码：

```
>app.greeting = 'Good morning'
<: You can not change greeting to Good morning
```

`setter` 运行成攻了。

#####methods
我们可以把我们需要在组件中使用的函数定义在这里，我们可以在 `{{ }}` 中调用它。修改我们的组件如下：

```javascript
let app = new Vue({
        el:'#app',
        template:`<div>
        <p>{{ say('hello') }} to {{ name }}</p>
        </div>`,
        data: function(){
            return {
                name:'Ucag'
            }
        },
        methods:{
            say: function(value){
                return value.toUpperCase()
            }
        }
    })
```
保存并在浏览器中打开，你会看到 `{{ }}` 成功调用了 `say` 函数。同样的，`methods` 中的函数会被绑定到组件上，可以使用 `this` 来访问它。

我们使用函数返回了一个经过处理之后的数据，并且接收了参数。那它和计算属性有什么不同呢？当`methods` 中的函数被调用时，每一次的结果都是函数**再次**运行之后的，也就是说，它的结果不会被缓存。我们可以把组件相关的 UI 动作定义在这里，比如在点击按钮之后需要执行的动作。

#####JavaScript表达式
刚才我们可以看到，`{{ }}` 中除了可以写我们需要访问的属性之外，还可以执行函数。其实，`{{ }}` 还可以写 javascript 表达式。
像下面这样也是正确的。
```javascript
{{ number + 1 }}
{{ ok ? 'YES' : 'NO' }}
{{ message.split('').reverse().join('') }}
```
####v-bind 与 v-on 
有的时候，我们希望能够对标签的属性有更多的控制。比如，动态的生成属性，触发我们自定义的事件动作。

重新编写我们的组件：

`grammer.html`
```javascript
let app = new Vue({
    el:'#app',
    template: `<div>
    <input 
    type="text" 
    placeholder="username" 
    v-on:input="changeHref">
    <a v-bind:href="UserLink">Go Home</a>
    </div>`,
    data:function(){
        return {
            UserLink:'#'
        }
    },
    methods:{
        changeHref: function(event){
            let username = event.target.value
            if (username){
                this.UserLink = 'http://www.example.com/' + username
            } else {
                this.UserLink = '#'
            }
        }
    }
})
```
保存并在浏览器中打开，尝试输入几个数据，你会看到这样的效果。
![绑定属性与事件]()，我们把在模板中，类似这样以`v-`开头的东西称为“指令”。

我们在标签的事件上使用了 `v-on:event="handler"` 语法，来告诉 Vue ，当 `event` 事件发生时，调用 `handler` 函数。 Vue 会默认的往这个函数里传一个 `event` 参数，`event` 代事件对象。我们使用 `v-bind:property="value"` 来告诉 Vue ，`property` 属性的值等于组件的 `value` 属性值。也就是说，如果你使用了 `v-on` 或者 `v-bind` 等，那么等号后面的东西就不再会被解释为字符串，而是一个 js 表达式。

他们都有自己的缩写形式，`v-bind:property="value` 可以写为 `:property=value`，`v-on:event="handler"` 可以写为 `@event="handler"`。所以像这样写也是可以的：

```javascript
let app = new Vue({
    ...
    template: `<div>
    <input 
    type="text" 
    placeholder="username" 
    @:input="changeHref">
    <a :href="UserLink">Go Home</a>
    </div>`,
    ...
})
```
####v-if 与 v-for
我们可以在 Django 的模板中使用 `{% for item in iterable %}` 来迭代对象，使用 `{% if conditino %}` 来做条件判断。同样的，Vue 也提供了这些功能。

把我们的组件重新编写如下：

```javascript
    let app = new Vue({
        el:'#app',
        template: `<ul>
        <li v-for="person in personList">
        <p>Name: {{ person.name }}</p>
        <p v-if="person.age > 18">Age: {{ person.age }}</p>
        </li>
        </ul>`,
        data:function(){
            return {
                personList:[
                {name:'Ucag',age:'18'},
                {name:'Ace',age:'20'},
                {name:'Lily',age:'22'}]
            }
        }
    })
```
保存并在浏览器中打开，你会看到浏览器渲染出了我们的列表。

`v-for` 用于迭代某个标签，指令的基本语法是：

```
<tag v-for="alias in expression"></tag>
```
`alias` 是当前迭代对象的别名。

当被迭代对象是 `Array` ，`string` ，`number` 时，可以使用以下两种语法迭代：
```
<tag v-for="alias in items"></tag>
<tag v-for="(item, index) in items"></tag>
```
在第二种迭代方式中，`index` 是其索引，也就是从 0 开始。

当迭代对象是 `Object` 时，可以使用以下三种方式迭代：
```
<tag v-for="val in objec"></tag>
<tag v-for="(val, key) in object"></tag>
<tag v-for="(val, key, index) in object"></tag>
```
第一种是直接迭代对象的**属性值**。第二种则包含了**属性值**和**属性**。第三种相对第二种多了一个索引值。

`v-if` 用于判断某个标签，基本语法是：
```
<tag v-if="conditino"></tag>
```
如果条件成立则渲染这个 `tag` ，不成立则不渲染。同样的，它还有自己其它的配套语法。
```
// 和 v-else 一起使用
<div v-if="conditino">
  Now you see me
</div>
<div v-else>
  Now you don't
</div>

//和 v-else-if 一起使用
<div v-if="type === 'A'">
  A
</div>
<div v-else-if="type === 'B'">
  B
</div>
<div v-else-if="type === 'C'">
  C
</div>
<div v-else>
  Not A/B/C
</div>
```
不过需要注意的是，`v-else` 或者 `v-else-if` 必须紧跟在 `v-if` 后使用，不然这些指令不会被识别。

当同时在一个标签中使用 `v-if` 与 `v-for` 时，总是会先执行 `v-for` ，再执行 `v-if`。也就是说，`v-for` 的优先级要高。


---
本节的 Vue 基础就讲完了。我们只是简单的入门了 Vue ，但是仅仅这些知识就已经够我们编写最基本的页面了。在下一节，我们将会运用前两节学到的知识，重构我们的 APP 。不过由于最近期末考试了，下一次更应该是在一月十号之后了。最后祝大家冬至快乐~






