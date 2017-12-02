//api
// 将 api 单独写在一起的好处包括但不限于：
//        1. 方便维护。不把 api 写死在相应动作下，一旦 api 有变动，直接在这里变动就好
//        2. 写成函数形式，这样可以动态的生成 api ，特别时对有 pk 或者 id 参数的 api 特别有用
//        3. 将 api 统一化管理，为以后的模块化做好拓展准备。
//        4. api 的语义清晰，大大降低人为应编码造成的错误。最常见的例子是忘了给 api 最后加上参数或者 / 。
const api = {
    v1: {  // api 版本号
        codes: { // api v1 版本下的 code api。
            list: function () { //获取实例查询集
                return '/api/v1/codes/'
            },
            detail: function (pk) { // 获取单一实例
                return `/api/v1/codes/${pk}/`
            },
            create: function () { // 创建实例
                return `/api/v1/codes/`
            },
            update: function (pk) { // 更新实例
                return `/api/v1/codes/${pk}/`
            },
            remove: function (pk) { //删除实例
                return `/api/v1/codes/${pk}/`
            },
            run: function () { //运行代码
                return '/api/v1/codes/run/'
            },
            runSave: function () {// 保存并运行代码
                return '/api/v1/codes/run/?save=true'
            },
            runSpecific: function (pk) { // 运行特定代码实例
                return `/api/v1/codes/run/${pk}/`
            },
            runSaveSpecific: function (pk) { // 运行并保存特定代码实例
                return `/api/v1/codes/run/${pk}/?save=true`
            }
        }
    }
};

//接下来的代码包含了前端中极其重要的设计思想，请大家认真学习。
//现在我们是在编写前端，所以需要大家从后端的思维模式中切换出来。前端，顾名思义，是为了
//展示数据而存在的，当数据发生变化时， 与数据相关联的 UI 也应该随着数据的变化而作出相应的动作。
//在我们的项目中，当我们点击运行按钮时，如果后端传来了输出数据，那么此时的输出框就应该作出相应的
//更新操作——将结果显示在浏览器上。所以，UI 的显示“状态”应该是以数据为基础的。数据变动则 UI 变动。
//所以，在前端中，把 UI 相关的数据称为 “状态” 。比如结果输出框就有两个状态，“显示结果”与“不显示结果”
//的状态，如何切换状态则取决于输出框想连接的数据有没有变动。
//以上，便是 “状态” 的概念。但是我们的 UI 怎么才能知道数据是否变动呢？那就是不断的查询相关的数据
//是否改变。那么问题就来了，我们应该怎么定义我们的数据呢？
//一种是把数据定义为全局变量，UI 不停的在全局变量中看这个值更新没有，更新了就刷新状态。看起来这样
//没什么毛病，但是当你的 UI 状态多起来之后问题就逐渐的显现了。到底该怎么命名状态才能清晰的表达
//每个状态的意思？到底怎么才能不让其他的变量名把我们的状态覆盖掉，不然出现莫名其妙的 bug？
//第二种是把数据单独放在一个单独的对象下。就像在浏览器中，所有的全局变量都放在 window 下一样，
//我们单独把状态变量放到一个变量中，然后访问这个变量就可以了。
//显然，我们应该采用第二种方法。那问题又来了，我们该怎么检测状态是否变化呢？
//一种是把检测的逻辑写在 UI 中，将上一次的值保存下来，然后不停对比状态的上一个值和当前值
//是否相同，不同就刷新 UI 。同样的，如果同一个状态变量有多种状态，那你的检测逻辑就需要
//考虑每种情况，然后依次写下来。这样做不仅很累人，而且也不够灵活。第二种，是给状态再加一个 sigin （签名）
//或者 signal （信号），当状态变动时，便发出状态改变的信号或者修改签名。这样，UI 只需要检测
//这个签名或者信号，只在发出改变信号时才会读取状态数据，作出相应的 UI 动作。
//显然，我们应该采用第二种方法。
//到这里或许已经有同学发现，这不是和我们后端的 Model 的概念很相似吗？是的，没错。它们两者
// 很相似。保持你的好奇心，在我们学 vue 时会继续深入这些概念。

//下面是一种实现方式，我们把储存状态的变量叫做  store，store 在英文中有储存的意思。
//同时我们的后端数据库也是用来储存数据的，叫这个名字很贴切。
//我们把不同的状态放在 store 每个状态有 state 和 changed 属性，state 用来储存 UI 相关联
//的变量信息，changed 作为状态是否改变的信号。UI 只需要监听 chagned 变量，当 changed 为 true
//时才读取并改变状态。
//我们目前的状态很少，也很简单。我们在下面先初始化他们

let store = {
    list: { //列表状态
        state: undefined,
        changed: false
    },
    detail: { //特定实例状态
        state: undefined,
        changed: false
    },
    output: { //输出状态
        state: undefined,
        changed: false
    }
};

//改变状态的动作
//这些动作负责调用 API ，并接受 API 返回的数据，然后将这些数据保存进 store 中。
//注意，在修改完状态之后，记得将状态的 changed 属性改为 true ,不然状态不会刷新到监听的 UI 上。

//从后端返回的数据中，把实例相关的数据处理成我们期望的形式，好方便我们调用
function getInstance(data) {
    let instance = data.fields;
    instance.pk = data.pk;
    return instance
}

//获取 code 列表，更改 list 状态
function getList() {
    $.getJSON({
        url: api.v1.codes.list(),
        success: function (data) {
            store.list.state = data.instances;
            store.list.changed = true;
        }
    })
}
//创建实例，并刷新 list 状态。
function create(code, name) {
    $.post({
        url: api.v1.codes.create(),
        data: {'code': code, 'name': name},
        dataType: 'json',
        success: function (data) {
            getList();
            alert('保存成功！');
        }
    })
}
//更新实例，并刷新 list 状态。
function update(pk, code, name) {
    $.ajax({
        url: api.v1.codes.update(pk),
        type: 'PUT',
        data: {'code': code, 'name': name},
        dataType: 'json',
        success: function (data) {
            getList();
            alert('更新成功！');
        }
    })
}
//获取实例，并刷新 detail 状态
function getDetail(pk) {
    $.getJSON({
        url: api.v1.codes.detail(pk),
        success: function (data) {
            let detail = getInstance(data.instances[0]);
            store.detail.state = detail;
            store.detail.changed = true;
        }
    })
}
//删除实例，并刷新 list 状态
function remove(pk) {
    $.ajax({
        url: api.v1.codes.remove(pk),
        type: 'DELETE',
        dataType: 'json',
        success: function (data) {
            getList();
            alert('删除成功！');
        }
    })
}
//运行代码，并刷新 output 状态
function run(code) {
    $.post({
        url: api.v1.codes.run(),
        dataType: 'json',
        data: {'code': code},
        success: function (data) {
            let output = data.output;
            store.output.state = output;
            store.output.changed = true;
        }
    })
}
//运行保存代码，并刷新 output 和 list 状态。
function runSave(code, name) {
    $.post({
        url: api.v1.codes.runSave(),
        dataType: 'json',
        data: {'code': code, 'name': name},
        success: function (data) {
            let output = data.output;
            store.output.state = output;
            store.output.changed = true;
            getList();
            alert('保存成功！');
        }
    })
}
//运行特定的代码实例，并刷新 output 状态
function runSpecific(pk) {
    $.get({
        url: api.v1.codes.runSpecific(pk),
        dataType: 'json',
        success: function (data) {
            let output = data.output;
            store.output.state = output;
            store.output.changed = true;
        }
    })
}
//运行并保存特定代码实例，并刷新 output 和 list 状态
function runSaveSpecific(pk, code, name) {
    $.ajax({
        url: api.v1.codes.runSaveSpecific(pk),
        type:'PUT',
        dataType: 'json',
        data: {'code': code, 'name': name},
        success: function (data) {
            let output = data.output;
            store.output.state = output;
            store.output.changed = true;
            getList();
            alert('保存成功！');
        }
    })
}

//UI 的动作逻辑

//使输入框随着输入内容变动大小
function flexSize(selector) {
    let ele = $(selector);
    ele.css({
        'height': 'auto',
        'overflow-y': 'hidden'
    }).height(ele.prop('scrollHeight'))
}
//将动态变动大小的动作绑定到输入框上
$('#code-input').on('input', function () {
    flexSize(this)
});

//渲染列表动作
function renderToTable(instance, tbody) {
    let name = instance.name;
    let pk = instance.pk;
    let options = `\
    <button class='btn btn-primary' onclick="getDetail(${pk})">查看</button>\
    <button class="btn btn-primary" onclick="runSpecific(${pk})">运行</button>\
    <button class="btn btn-danger" onclick="remove(${pk})">删除</button>`;
    let child = `<tr><td class="text-center">${name}</td><td>${options}</td></tr>`;
    tbody.append(child);
}

//渲染代码选项

//当点击查看代码时，渲染代码选项的动作

//我们使用模板字符串来让每个按钮能出发相应的状态修动作
function renderSpecificCodeOptions(pk) {
    let options = `\
    <button class="btn btn-primary" onclick="run($('#code-input').val())">运行</button>\
    <button class="btn btn-primary" onclick=\
    "update(${pk},$('#code-input').val(),$('#code-name-input').val())">保存修改</button>\
    <button class="btn" onclick=\
    "runSaveSpecific(${pk}, $('#code-input').val(), $('#code-name-input').val())">保存并运行</button>\
    <button class="btn btn-primary" onclick="renderGeneralCodeOptions()">New</button>`;
    $('#code-options').empty().append(options);// 先清除之前的选项，再添加当前的选项
}

//当点击新建代码时，渲染代码选项的动作
function renderGeneralCodeOptions() {
    let options = `\
    <button class="btn btn-primary" onclick="run($('#code-input').val())">运行</button>\
    <button class="btn btn-primary" onclick=\
    "create($('#code-input').val(),$('#code-name-input').val())">保存</button>\
    <button class="btn btn-primary" onclick=\
    "runSave($('#code-input').val(),$('#code-name-input').val())">保存并运行</button>\
    <button class="btn btn-primary" onclick="renderGeneralCodeOptions()">New</button>`;
    $('#code-input').val('');// 清除输入框
    $('#code-output').val('');// 清除输出框
    $('#code-name-input').val('');// 清除代码片段名输入框
    flexSize('#code-output');// 由于我们在改变输入、输出框的内容时并没有出发 ‘input’ 事件，所以需要手动运行这个函数
    $('#code-options').empty().append(options);// 清除的之前的选项，再添加当前的选项
}

//UI 监听逻辑
// watcher 会迭代 store 的每个属性，一旦某个状态发生改变，就会执行相应的 UI 动作
//记得，在执行完相应的 UI 动作后，要把 changed 状态改回去，不然 UI 会一直不断的刷新，刷新会
//根本停不下来。你看到的 UI 会在一瞬间就会替换为下一个 UI。
function watcher() {
    for (let op in store) {
        switch (op) {
            case 'list':// 当 list 状态改变时就刷新页面中展示 list 的 UI，在这里，我们的 UI 一个 <table> 。
                if (store[op].changed) {
                    let instances = store[op].state;
                    let tbody = $('tbody');
                    tbody.empty();
                    for (let i = 0; i < instances.length; i++) {
                        let instance = getInstance(instances[i]);
                        renderToTable(instance, tbody);
                    }
                    store[op].changed = false; // 记得将 changed 信号改回去哦。
                }
                break;
            case 'detail':
                if (store[op].changed) {// 当 detail 状态改变时，就更新 代码输入框，代码片段名输入框，结果输出框的状态
                    let instance = store[op].state;
                    $('#code-input').val(instance.code);
                    $('#code-name-input').val(instance.name);
                    $('#code-output').val('');// 记得请空上次运行代码的结果哦。
                    flexSize('#code-input');// 同样的，没有出发 'input' 动作，就要手动改变值
                    renderSpecificCodeOptions(instance.pk);// 渲染代码选项
                    store[op].changed = false;// 把 changed 信号改回去
                }
                break;
            case 'output':
                if (store[op].changed) { //当 output 状态改变时，就改变输出框的的状态。
                    let output = store[op].state;
                    $('#code-output').val(output);
                    flexSize('#code-output');// 记得手动调用这个函数。
                    store[op].changed = false // changed 改回去
                }
                break;
        }
    }
}
//将UI主逻辑添加到时间队列中

getList();// 初始化的时候我们应该手动的调用一次，好让列表能在页面上展示出来。
renderGeneralCodeOptions();// 手动调用一次，好让代码选项渲染出来
setInterval("watcher()", 500);// 将 watcher 设置为 500 毫秒，也就是 0.5 秒就执行一次，
// 这样就实现了 UI 在不断的监听状态的变化。


