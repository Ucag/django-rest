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
    },
})