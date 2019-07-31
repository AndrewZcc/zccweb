2019.7.30

## sqlAlchemy 排序

* https://www.cnblogs.com/chen0427/p/8783688.html
* https://stackoverflow.com/questions/25948991/sqlalchemy-order-by-on-backref

```python
def logout():
    if session.get('w3account'):
        session.pop('w3account')
    return redirect(url_for('main.homepage'))
    
class Document(db.Model):
    author = db.relationship('User', backref=db.backref('documents', order_by='Document.create_time'))
    tags = db.relationship('Category', secondary=doc_tag, backref=db.backref('documents', order_by='Document.create_time'))
```


## 基本工具

```python
# db定义时请注意：(关闭autoflush)
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(session_options={"autoflush": False})

# 使用
url_id = generate_random_str(12)
while 1:
doc = Document.query.filter(Document.url_id == url_id).first()
if not doc:
    break
url_id = generate_random_str(12)
#print("loc2: %s" % url_id)
new_doc.url_id = str(url_id)

# 生成随机数字和字母组合字符串
def generate_random_str(randomlength=16):
    """
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str
```

2019.7.27

## 个人网站首页

* 首页设计

`base.html`
```html
方案一：(直接修改图标链接)
<a class="navbar-brand" href="https://zhchuch.github.io/" target="_blank">Welcome to PNF platform!</a>
<a class="navbar-brand" href="https://zhchuch.github.io/" target="_blank">Objective Management</a>

方案二：(在首页额外添加导航入口)
* 不要爬html数据过来了，个人主页就用Github静态页面就ok了！
```

2019.7.21

## 导航栏设计

* base.html

```html
<div id="wrapper">
	<nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
		<div class="navbar-header"> LOGO </div>
		<ul class="nav navbar-top-links navbar-left">...</ul>
		<ul class="nav navbar-top-links navbar-right">...</ul>
		<div class="navbar-default sidebar" role="navigation">
			<div class="sidebar-nav navbar-collapse">
				<ul class="nav" id="side-menu">
				...
				</ul>
			</div>
		</div>
	</nav>
	---------
	<div id="page-wrapper">
		{% block content %}{% endblock %}
	</div>
	---------
	<div class="img_return_top">
		<img src="{{ url_for('static', filename='images/back2Top.png') }}" alt="返回顶部" title="返回顶部">
	</div>
</div>
```

* 返回顶部

base.css

```css
.img_return_top {
    cursor: pointer;
    position: fixed;
    right: 30px;
    bottom: 20px;
    display: none;
}
```

base.js

```js
function showScroll(imgBackTop) {
    $(window).scroll(function () {
        var scrollValue = $(window).scrollTop();
        scrollValue > 100 ? imgBackTop.fadeIn() : imgBackTop.fadeOut();
    });

    imgBackTop.click(function () {
            $("html,body").animate({scrollTop: 0}, 200);
        }
    );
}

var imgBackTop = $('.img_return_top');

showScroll(imgBackTop);
```

## Editor.md 集成

* 目录包

```shell
➜  sophonzcc git:(DevelopBranch) ll webpage/static/editormd
total 496K
drwxr-xr-x  2 root root 4.0K Jul 18 16:33 css
-rw-r--r--  1 root root 163K Jul 18 16:33 editormd.amd.js
-rw-r--r--  1 root root  55K Jul 18 16:33 editormd.amd.min.js
-rw-r--r--  1 root root 160K Jul 18 16:33 editormd.js
-rw-r--r--  1 root root  53K Jul 18 16:33 editormd.min.js
drwxr-xr-x  2 root root 4.0K Jul 18 16:33 fonts
-rw-r--r--  1 root root  13K Jul 18 16:33 Gulpfile.js
drwxr-xr-x  2 root root 4.0K Jul 18 16:33 languages
drwxr-xr-x  3 root root 4.0K Jul 18 16:33 lib
drwxr-xr-x 13 root root 4.0K Jul 18 16:33 plugins
drwxr-xr-x  3 root root 4.0K Jul 18 16:33 scss
drwxr-xr-x  2 root root 4.0K Jul 18 16:33 src
```

* 编辑器

```html
{% block link %}
<link rel="stylesheet" href="{{ url_for('static', filename='editormd/css/editormd.css') }}" />
{% endblock %}

<div class="form-container">
	<form action="{{ url_for('main.edit_doc', cat_id= catid, doc_id= docid) }}" method="POST" enctype="multipart/form-data">
		<label for="mkinput">请编辑文档内容 (markdown 格式)</label>
		<div class="form-group" id="my-editor-md">
		<textarea name="updateContent" id="mkinput" rows="30" class="form-control" placeholder="文档内容">{{ doccontent }}</textarea>
		</div>
		<div class="form-group" style="float: left;">
		<button type="submit" class="btn btn-success">确认修改</button>
		</div>
	</form>
	<form action="{{ url_for('main.category', cat_id= catid) }}" method="GET" style="float: left; padding-left: 10px">
		<div class="form-group">
		<button type="submit" class="btn btn-primary">放弃修改</button>
		</div>
	</form>
</div>

{% block jsscript %}
<script src="{{ url_for('static', filename='editormd/editormd.min.js') }}"></script>
<script type="text/javascript">
    var sidebar = document.getElementsByClassName("sidebar")[0];

    $(function() {
        var editor = editormd("my-editor-md", {
            width  : "100%",
            height : 650,
            path   : "/static/editormd/lib/",
            onfullscreen : function() {
                //alert("onfullscreen");
                sidebar.style.display = "none";
            },
            onfullscreenExit : function () {

                sidebar.style.display = "";
            }
        });
    });
</script>
{% endblock %}
```

* HTML渲染

```html
{% block link %}
    <link rel="stylesheet" href="{{ url_for('static', filename='editormd/css/editormd.preview.css') }}" />
{% endblock %}

{% block content %}
    <div class="row">
        <div id="doc-content">
            <textarea style="display:none;">{{ md_data }}</textarea>
        </div>
	</div>
{% endblock %}

{% block jsscript %}
    <script src="{{ url_for('static', filename='editormd/lib/marked.min.js') }}"></script>
    <script src="{{ url_for('static', filename='editormd/lib/prettify.min.js') }}"></script>
    <script src="{{ url_for('static', filename='editormd/lib/raphael.min.js') }}"></script>
    <script src="{{ url_for('static', filename='editormd/lib/underscore.min.js') }}"></script>
    <script src="{{ url_for('static', filename='editormd/lib/sequence-diagram.min.js') }}"></script>
    <script src="{{ url_for('static', filename='editormd/lib/flowchart.min.js') }}"></script>
    <script src="{{ url_for('static', filename='editormd/lib/jquery.flowchart.min.js') }}"></script>

    <script src="{{ url_for('static', filename='editormd/editormd.min.js') }}"></script>

    <script type="text/javascript">
        var testEditor;
        $(function () {
            testEditor = editormd.markdownToHTML("doc-content", {
                htmlDecode: "style,script,iframe",
                emoji: true,
                taskList: true,
                tex: true,
                flowChart: true,
                sequenceDiagram: true,
                codeFold: true,
        });});
     </script>
{% endblock %}
```

----

### The *END*.
