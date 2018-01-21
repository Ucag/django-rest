前后端分离的好处就是可以使前端和后端的开发分离开来，如果使用 Django 的模板系统，我们需要在前端和后端的开发中不停的切换，前后端分离可以把前端项目和后端项目分离开来，各自建立项目单独开发。那么问题来了，前端怎么建项目？这就是本章需要解决的问题。

对于任何的工具，我的哲学是“工具为人服务，而不是人为工具服务”，希望大家不要为了学习某个工具而学习，任何工具的出现都是为了满足不同的需求。这是在学习前端工具链时需要牢记的一点，不然等学完了，学的东西就全部忘了。前端的世界浩瀚无比，小小的一章并不能很详尽的介绍它们，仅仅是作为一个入门的介绍，但是对于我们来说一定是够用的。

##JavaScript 的解释器 —— node 与 “模块化”

js 和 python 同为脚本语言，他们都有自己的解释器。js 的解释器是 node 。

在 node 出现前 js 有没有自己的解释器呢？有的，那就是我们的浏览器中的 js 引擎，但是这个引擎的实现仅仅是针对浏览器环境的，这个引擎限制了 js 的很多功能，比如 js 在浏览器引擎下都不能进行文件的读写，当然这么做是为了用户的安全着想。如果我们想要用 js 实现 python 的许多功能呢？这时就需要 node 了。

先去[这里](http://nodejs.cn/download/)下载 node ，像安装 python 一样把 node 安装到你的电脑上，记得把安装路径添加到环境变量中。这些都是和安装 python 是一样的。

python 运行 `.py` 脚本是 `python <filename>.py` 命令，node 也是同理， `node <filename>.js` 就可以运行一个 js 脚本了。

在上一章，我们在写 `index.js` 时需要考虑代码编写的顺序，这是一件烦人的事情。等到以后代码量大起来，谁知道哪个组件引用了哪个组件，还容易出现 undefined 错误。要是我们能单独把组件都写在一个地方，要用他们的时候再按照需求引入就好了。也就是，我们希望能够进行“模块化”开发。不用去考虑代码顺序，做到代码解耦。

js 被创建的时候并没有考虑到模块化开发，因为当时的需求还是很简单的，随着需求变多，模块化开发成了必须。我们知道，我们可以在 python 中使用 import  来引入我们需要的包和库。 由于在 es6 之前还没有官方提供这个功能，于是 js 社区就自己实现了这项需求。这就是 `require` 和 `module.exports` 的故事，也就是 CommonJS 规范。

在 python 中，我们直接使用 `import` 就可以从一个包中直接导入我们需要的东西。但是 js 有些不同，js 需要被导入的包主动导出内部变量，然后其它的包才能导入他们。

在 CommonJS 规范中，每一个模块都默认含有一个全局**变量** `module` ，它有一个 `exports` 属性，我们可以通过这个属性来向外暴露内部的变量。`module.exports` 的默认值为一个空对象。外部可以通过全局的 `require` 函数来导入其它包内的 `module.exports` 变量。

```javascript
// A.js
function out(){
    console.log('model A.')
} 
 
module.exports = out // 导出 out 函数

// B.js
const out = require('./A') // 从 A.js 引入 out
out()
```

在终端里输入 `node B.js` ，你就会看到控制台打印出了 `model A.` 。

就这么简单。和 Python 的差别就是 js 需要你主动导出变量。这也是 node 引用模块的方法。

如果你不想写 `module.exports` ，还有另外一个全局变量 `exports` 供你使用，它是 `module.exports` 的**引用**，由于 `module.exports` 的默认值为一个空对象，所以它的默认值也是一个空对象。如：

```javascript
// A.js
exports.a = 'a';
exports.b = function(){
    console.log('b')
}

// B.js
const A = require('./A')
console.log(A.a) // 'a'
A.b() // 'b'
```

有时候我们的模块不止一个文件，而是有很多个文件。我们可以直接使用 `require` 来引入模块路径，`require` 会自动搜寻引入目录下的 `index.js` 文件，它会把这个文件作为整个模块的入口。如：

```
// 模块 ucag
ucag/
    index.js // module.exports = {
        name: require('./name').name,
        age: require('./age').age,
        job: require('./job').job
    }

    age.js // exports.age = 18
    name.js // exports.name = 'ucag'
    job.js // exports.job = 'student'
```
我们在一个文件里引入：
```javascript
const ucag = require('./ucag')
ucag.name // 'ucag'
ucag.age // 18
ucag.job // 'student'
```


在 es6 之后，js 有了自己引用模块的方法，它有了自己的 `import` 和 `export` **关键字**。对外导出用 `export` ，对内引入用 `import`。

对于导出，需要遵循以下语法：
```javascript
export expression
    // 如：
        export var a = 1, b = 2;  // 导出 a 和 b 两个变量

export {var1, var2, ...} //var1 var2 为导要出的变量

export { v1 as var1, v2 as var2} // 使用 as 来改变导出变量的名字

```
不过需要注意的是，当我们只想导出一个变量时，我们不能这么写：

```javascript
let a = 1;
export a; // 这是错误的写法
export { a } // 这才是正确的写法
```

我们可以这样来引入：

```javascript
import { var1 }from 'model' // 从 model 导出 var1 变量
import {v1, v2 } from 'model' // 从 model 导出多个变量
import { var1 as v1 }from 'model'  // 从 model 导出 var1 变量并命名为 v1
import * as NewVar from 'model' // 从 model 导入全部的变量
```

在使用 `import` 时，`import` 的变量名要和 `export` 的变量名完全相同，但是有时候我们我们并不知道一个文件导出的变量叫什么名字，只知道我们需要使用这个模块默认导出的东西，于是便出现了 `default` 关键字的使用。我们可以在 `export` 时使用这个关键字来做到“匿名”导出，在 `import` 时，随便取个变量名就可以了。

```javascript
export default expression
    // 如：
    export default class {} // 导出一个类
    export default {} //导出一个对象
    export default function(){} //导出一个函数

```

我们可以这样来引入：

```javascript
import NewVar from 'model' // NewVar 是我们为 export default 导出变量取的名字。
```

注意，默认导出和命名导出各自的导入是有区别的：
```javascript
// 默认导出
export default {
    name:'ucag'
}
// 默认导出对应导入
import AnyVarName from 'model' // 没有花括号
AnyVarName.name // 'ucag'

//命名导出
export var name='ucag'
//命名导出对应导入
import { name } from 'model' // 有花括号
name // 'ucag'

//两种导出方式同时使用
export default {
    name:'ucag'
}
export var age=18;

//两种导入
import NameObj from 'model' //导入默认导出
import { age } from 'model' //导入命名导出

NameObj.name // 'ucag'
age // 18
```

总结一下：

1. 目前我们学了两种模块化的方式。他们是 CommonJS 的模块化方式与 es6 的模块化方式。两种方式不要混用了哦。
2. CommonJS 规范：
    1. 使用 `module.exports` 或 `exports` 来导出内部变量
    2. 使用 `require` 导入变量。当被导入对象是路径时，`require` 会自动搜寻并引入目录下的 `index.js` 文件，会把这个文件作为整个文件的入口。
3. es6 规范：
    1. 使用 `import` 与 `export` 来导出内部变量
    2. 当导入命名导出变量时，使用基于 `import { varName } from 'model'` 的语法；当导入匿名或默认导入时，使用 `import varName from 'model'` 语法；

悲催的是，node 只支持 CommonJS 方式来进行模块化编写代码。

##前端的 pip —— npm

刚才我们讲了模块化，现在我们就可以用不同的模块做很多事情了。 我们可以使用 pip 来安装 python 的相关包，在 node 下，我们可以使用 npm 来安装我们需要的库。当然，安装包的工具不止有 npm 一种，还有许多其它的包管理工具供我们使用。现在的 python 已经在安装时默认安装了 pip ，node 在安装时已经默认安装了 npm ，所以我们就用这个现成的工具。

前端项目有个特点 —— 版本更替特别快。今天页面是一个样子，明天可能就换成另外的样子了，变化特别频繁，可能今天的依赖库是一个较低的版本，明天它就更新了。所以需要把依赖的库和项目放在一起，而不是全局安装到 node 环境中。每开发一个新项目就需要重新安装一次依赖库。而真正的 node 环境下可能是什么都没有的，就一个 npm 。

在一个前端项目中，总是会把依赖库放进一个文件夹里，然后从这个文件夹里导入需要的库和依赖，这个文件夹叫做 `node_modules` 。

在 pip 中，我们可以使用 `requirements.txt` 来记录我们的项目依赖。在 npm 下，我们使用 `package.json` 来记录依赖。当我们在 `package.json` 中写好需要的依赖后，在同一路径下运行 `npm install`， npm 会自动搜寻当前目录下的 `package.json` 并且自动安装其中的依赖到 `node_modules` 中，要是当前目录没有 `node_modules` 目录，npm 就会帮我们自己创建一个。当我们想要使用别人的项目时，直接把他们的 `package.json` 拷贝过来，再 `npm install` 就可以完成开发环境的搭建了。这样是不是特别的方便。

当你在运行完了 `npm install` 时，如果在以后的开发中想要再安装新的包，直接使用 `npm install <your-package>` 安装新的包就行了，npm 会自动帮你把新的包装到当前的 `node_modules` 下。

在我们发布一个 python 项目时，我们对于依赖的说明通常是自己写一个 `requirements.txt` ，让用户们自己去装依赖。 npm 为我们提供了更加炫酷的功能。在开发项目时，你直接在含有 `package.json` 的目录下运行 `npm install <your-package> --save-dev` ，npm 会自动帮你把依赖写到 `package.json` 中。以后你就可以直接发布自己的项目，都不用在 `package.json` 中手写依赖。

通过上面的内容我们知道，我们只需要在一个文件夹中创建好 `package.json` ，就可以自动安装我们的包了。 我们还可以使用 npm 自动生成这个文件。在一个空目录下，运行 `npm init` ，npm 会问你一些有的没的问题，你可以随便回答，也可以一路回车什么都不答，目录下就会自动多一个 `package.json` 文件。比如我们在一个叫做 vue-test 的路径下运行这个命令，记得以**管理员**权限运行。

```
λ npm init
This utility will walk you through creating a package.json file.
It only covers the most common items, and tries to guess sensible defaults.

See `npm help json` for definitive documentation on these fields
and exactly what they do.

Use `npm install <pkg>` afterwards to install a package and
save it as a dependency in the package.json file.

Press ^C at any time to quit.
package name: (vue-test)
version: (1.0.0)
description:
entry point: (index.js)
test command:
git repository:
keywords:
author:
license: (ISC)
About to write to C:\Users\Administrator\Desktop\vue-test\package.json:

{
  "name": "vue-test",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC"
}


Is this ok? (yes)

```

如果你不想按回车，在运行 `npm init` 时加一个 `-y` 参数，`npm` 就会默认你使用它生成的答案。也就是运行 `npm init -y` 就行了。
```
λ npm init -y
Wrote to C:\Users\Administrator\Desktop\vue-test\package.json:

{
  "name": "vue-test",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

然后在以后的安装中，我们使用 `npm install --save-dev` ，就会自动把依赖库安装到 `node_modules` 中，把相关库依赖的版本信息写入到 `package.json` 中。

还是以刚才的 vue-test 为例，在创建完了 `package.json` 后，运行：

```
λ npm install --save-dev jquery
npm notice created a lockfile as package-lock.json. You should commit this file.
npm WARN vue-test@1.0.0 No description
npm WARN vue-test@1.0.0 No repository field.

+ jquery@3.2.1
added 1 package in 5.114s
```

此时，我们发现又多了一个 `package-lock.json`文件， 先不管它。我们再打开 `package.json` 看看，你会发现它的内容变成了这样：
```
λ cat package.json
{
  "name": "vue-test",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "jquery": "^3.2.1"
  }
}
```

依赖已经自动写入了 `package.json` 中。我们再删除 `node_modules` 文件夹和 `package-lock.json` ，只留下 `package.json` 。再运行 `npm install`。
```
λ npm install
npm notice created a lockfile as package-lock.json. You should commit this file.
npm WARN vue-test@1.0.0 No description
npm WARN vue-test@1.0.0 No repository field.

added 1 package in 5.4s
```
我们发现 npm 已经为我们安装好了依赖。

当然，我们有时需要一些各个项目都会用到的工具。还是以 python 为例，我们会使用 `virtualenv` 来创建虚拟环境，在安装它时，我们直接全局安装到了系统中。npm 也可以全局安装我们的包。在任意路径下，使用 `npm install -g <your-package>` 就可以全局安装一个包了。我们在以后会用到一个工具叫做 `vue-cli` ，我们可以用它来快速的创建一个 vue 项目。为什么要用它呢，在前端项目中，有一些库是必须要用到的比如我们的 `webpack` ，比如开发 vue 需要用到的 `vue` 包，`vue-router`，`vuex` 等等，它会帮我们把这些自动写入 `package.json` 中，并且会为我们建立起最基本的项目结构。就像是我们使用 `django-admin` 来创建一个 Django 项目一样。这样的工具，在前端被称为**“脚手架”**。

任意路径下运行：
```
npm install -g vue-cli
```
vue 脚手架就被安装到了我们的 node 环境中。我们就可以在命令行中使用 `vue` 命令来创建新的项目了，不需要自己手动创建项目。大家可以试着运行 `vue --help` ，看看你是否安装成功了 `vue-cli`。
```
λ vue --help

  Usage: vue <command> [options]


  Options:

    -V, --version  output the version number
    -h, --help     output usage information


  Commands:

    init        generate a new project from a template
    list        list available official templates
    build       prototype a new project
    help [cmd]  display help for [cmd]
```

npm 除了可以安装包之外，还可以使用 `npm run` 用来管理脚本命令。
还是以刚才安装 'jquery' 的包为例，打开 `package.json` ，把 `scripts` 字段改成这样：
```json
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "vh": "vue --help"
  }
```
然后在 `package.json` 路径下运行 `npm run vh` ，你就会看到控制台输出了 vue 脚手架的帮助信息。

当我们运行 `npm run <cmd>`时，npm 会搜寻同目录下的 `package.json` 中的 `scripts` 中对应的属性，然后把当前的 `node_modules` 加入环境变量中，执行其中命令，这样就不用我们每次都都手动输入长长的命令了。

还是总结一下：

1. npm 是 node 中的包管理工具。
2. `npm install`： 安装 `package.json` 中的依赖到 `node_modules` 中。
3. `npm install <package-name> --save-dev`：把包安装到 `node_modules` 中，并把包依赖写入 `package.json` 中。
4. `npm install <package-name> -g`：全局安装某个包。
5. `npm run <cmd>`： 运行当前目录下 `package.json` 的 `scripts` 中的命令。


##前端工具链
前端开发会用到许许多多的工具，有的工具是为了更加方便的开发而生，有的工具是为了使代码更好的适应浏览器环境。每个工具的出现都是为了解决特定的问题。
###解决版本差异 —— babel
版本差异一直是个很让人头痛的问题。用 python2 写的代码，大概率会在 python3 上运行失败。 js 是运行在浏览器上的，很多的浏览器更新并没有能够很稳定的跟上 js 更新的步伐，有的浏览器只支持到 es5 ，或者只支持部分 es6 特性。为了能够向下兼容，大家想了办法 —— 把 es6 的代码转换为 es5 的代码就行了！开发的时候用 es6 ，最后再把代码转换成 es5 代码就行了！于是便出现了 babel 。

创建一个叫做 `babel-test` 的文件夹，在此路径下运行：
```
npm init -y
npm install --save-dev babel-cli
```

在使用 babel 前，我们需要通过配置文件告诉它转码规则是什么。babel 默认的配置文件名为 `.babelrc`。
在 `babel-test` 下创建 `.babelrc`，写入：
```json
  {
    "presets": [
      "es2015"
    ],
    "plugins": []
  }
```
转码规则是以附加规则包的形式出现的。所以在配置好了之后我们还需要安装规则包。
```
npm install --save-dev babel-preset-es2015
```
babel 是以命令行的形式使用的，最常用的几个命令如下：
```
# 转码结果打印到控制台
 babel es6.js

# 转码结果写入一个文件
 babel es6.js -o es5.js # 将 es6.js 的转码结果写入 es5.js 中

# 转码整个目录到指定路径
 babel es6js -d es5js # 将 es6js 路径下的 js 文件转码到 es5js 路径下
```
但是由于我们的 babel 是安装在 babel-test 的 `node_modules` 中的，所以需要使用 `npm run` 来方便运行以上命令。

编辑 `package.json`：
```json
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "build": "babel inputs -d outputs"
  }
```

在 babel-test 下创建一个新的目录 inputs ，在其中写入新的文件 a.js:
```javascript
// es6 语法，模板字符串
let name = 'ucag'
let greeting = `hello my name is ${name}`
```
然后运行：
```
npm run build
```
在转换完成之后，我们在 outputs 下找到 a.js，发现代码变成了这样：
```javascript
'use strict';

var name = 'ucag';
var greeting = 'hello my name is ' + name;
```
es6 代码已经被转换为了 es5 代码。

###整合资源 —— webpack
在一个前端项目中，会有许许多多的文件。更重要的是，最后我们需要通过浏览器来运行他们。我们用 es6 写的代码，需要转换一次之后才能上线使用。如果我们用的是 TypeScript 写的 js ，那我们还需要先把 TypeScript 转换为原生 js ，再用 babel 转换为 es5 代码。如果我们使用的是模块化开发，但是浏览器又不支持，我们还需要把模块化的代码整合为浏览器可执行的代码。总之，为了方便开发与方便在浏览器上运行，我们需要用到许许多多的工具。

webpack 最重要的功能就是可以把相互依赖的模块打包。我们在模块化开发之后，可能会产生许多的 js 文件，要是一个个手写把他们引入到 html 中是一件很麻烦的事情，所以我们此时就需要 webpack 来帮我们把分离的模块组织到一起，这样就会方便很多了
创建一个新的路径 webpack-test ，在此路径下运行：
```
npm init -y
npm install --save-dev webpack
```

使用前先配置，在配置之前我们需要知道一些最基本的概念。

1. 入口 entry：不管一个项目有多复杂，它总是有一个入口的。这个入口就被称为 entry 。这就像是我们的模块有个 `index.js` 一样。
2. 出口 output：webpack 根据入口文件将被依赖的文件按照一定的规则打包在一起，最终需要一个输出打包文件的地方，这就是 output 。

这就是最基本的概念了，我们会在以后的教程中学习到更多有关 webpack 配置的知识，不过由于我们目前的需求还很简单，还用不到其它的一些功能，就算是现在讲了也难以体会其中的作用，所以我们目前不着急，慢慢来。

webpack 有多种加载配置的方法，一种是写一个独立的配置文件，一种是在命令行内编写配置，还有许多其它更灵活编写配置的方法，我们以后再说。当我们在 webpack-test 下不带任何参数运行 `webpack` 命令时，`webpack` 会自动去寻找名为 `webpack.config.js` 的文件，这就是它默认的配置文件名了。

在 webpack-test 下创建一个新的文件 `webpack.config.js`:
```javascript
module.exports = {
    entry:'./main.js', // 入口文件为当前路径下的 main.js 为文件
    output:{
        path:__dirname, // __dirname 是 node 中的全局变量，代表当前路径。
        filename:'index.js' // 打包之后的文件名
    }
}
```


编辑 `package.json` ：
```json
"scripts"{
    'pkg':'webpack' // 编辑快捷命令
}
```

以第三章的 index.js 为例，当时我们把所有的代码都写到了一个文件中，现在我们可以把他们分开写了，最后再打包起来。

创建几个新文件分别为 `components.js` `api.js` `store.js` `main.js` `vue.js` `jquery.js` 

`vue.js`: vue 源文件
`jquery`： jquery 源文件

`api.js`:
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

module.exports = api // 导出 API 
```

`store.js`
```javascript
const $ = require('./jquery') // 引入 jquery 

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

module.exports = store // 导出 store
```

`components.js`
```javascript
const store = require('./store')
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

module.exports = {
    list, input, output, options
} // 导出组件
```

`main.js`
```javascript
const cmp = require('./components') //引入组件
const list = cmp.list
const options = cmp.options
const input = cmp.input
const output = cmp.output
const Vue = require('./vue')

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

let root = new Vue({ //根组件，整个页面入口
    el: '#app',
    template: '<app></app>',
    components: {
        'app': app
    }
})
```

在 webpack-test 下运行：
```
npm run pkg # 运行 webpack
```

过一会儿你就会发现多了一个 `index.js` 文件，这就是我们打包的最终结果了。 6 个 js 文件被打包成了一个文件，最终打包的 `index.js` 的功能和那 6 个 js 文件的功能都是一样的。并且浏览器可以正常执行这些代码， webpack 已经为我们整合好代码，浏览器中不会出现模块化支持的问题。我们只需要在

要是你把 `index.js` 放到我们的 `index.html` 里，先不引入 `bootstrap` ，你会发现页面还是可以正常使用的。功能和前面完全相同！如果我们不使用 webpack ，那么我们需要在 html 页面按照顺序挨着写 `<script src=""></script>` 。

---
本章前端工具链的部分就简单的介绍到这里。我们并没有打包 bootstrap.js ，
那 bootstrap 该怎么办呢？如果我们只是简单的把 bootstrap.js 和我们打包到一起你会发现还是会报错。这是 webpack 的问题吗？这是我们之后要解决的问题。保持你的好奇心。




















