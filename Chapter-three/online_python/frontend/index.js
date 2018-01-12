//管理 API 
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

//Store
//Store中包含了 state 和 actions ，这些操作都是和数据直接相关的。
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

