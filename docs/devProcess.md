## 所遇问题列表

1. Python 环境设置

    ```shell
    # 切换 python 默认版本
    $ vim ~/.bash_profile
    alias python="/usr/local/bin/python3"
    #alias python="/usr/bin/python2.7"
    alias pip="/usr/local/bin/pip3"
    #alias pip="/usr/local/bin/pip2"
    
    $ source ~/.bash_profile
    ```

1. **Fixed**: 遗留问题：怎么用 lazypinyin 获取安全字符串？

    ```python
    from werkzeug.utils import secure_filename
    from pypinyin import lazy_pinyin
    
    todostr = request.form.get('todostr')
    sec_str = secure_filename("".join(lazy_pinyin(todostr)))
    ```

1. python-flask项目 **端口设置无效**
    
    https://www.cnblogs.com/xiaodai0/p/10460751.html
    <br>（解决方案：用 python解释器 运行，使用生产环境[Production],而非默认的开发环境[Development]）
    
1. 当 8090端口 被占用时

    - 使用 `app.run(host='0.0.0.0', port='8090')` 不会报错，但 浏览器访问时 会报 `405 Not Allowed` 错误；
    - 建议 首次运行新项目用 `app.run(host='127.0.0.1', port='8090')` 先尝试运行，如果该端口已被占用，使用该命令会提供报错信息！

1. 按钮添加弹出框（确认弹框）

    ```html5
    <input type="submit" class="btn btn-danger" value="删除" onclick="return confirm('确认删除文档吗？（该操作不可撤回）')">
    ```
    
1. Error: sqlalchemy.exc.IntegrityError (sqlalchemy query filter raised as a result of Query-invoked autoflush)

    * 在使用 sqlalchemy.filter.query 时，由于 SqlAlchemy 默认开启了 auto-flush(预创建) 功能，所以对于 nullable=Flase (非空字段) 查询就遇到如上报错
    * 解决方法：（创建db时，关闭autoflush功能）

        ```python
        from flask_sqlalchemy import SQLAlchemy
        
        db = SQLAlchemy(session_options={"autoflush": False})
        ```

1. 如何让sidebar左侧边栏导航在垂直方向全尺寸拉伸？

    https://blog.csdn.net/qq_35393869/article/details/88043093
    
    ```css
    ✖️height: calc(100% - 10px);
    ✔️height: calc(100vh - 48px);
    ```
    
    侧边栏 Corp-Web Usage:
    
    ```html
    <!-- Custom CSS -->
    <link href="{{ url_for('static', filename='custom/sb-admin-2.css') }}" rel="stylesheet">

    <div class="navbar-default sidebar" role="navigation">
    <div class="sidebar-nav navbar-collapse">
    <ul class="nav" id="side-menu">
    <li class="sidebar-search">
    <div class="input-group custom-search-form">
    <input type="text" class="form-control" placeholder="搜一下" disabled="true">
    <span class="input-group-btn">
    <button class="btn btn-default" type="button" disabled="true">
    <i class="fa fa-search"></i>
    </button>
    </span>
    </div>
    <!-- /input-group -->
    </li>
    <li>left sidebar items.</li>
    <li class="baseLeftNavLi">
    <a href="/feedback"><i class="fa fa-edit fa-fw"></i> 反馈</a>
    </li>
    </ul>
    </div>
    </div>
    ```

    • **参考的模板 网站（SB Admin v2.0）**
    <br>http://www.suchso.com/code/sbadminiframe/sbadmin/pages/index.html
    <br>https://technext.github.io/startbootstrap-sb-admin-2/pages/index.html 【网站效果】
    <br>https://github.com/technext/startbootstrap-sb-admin-2 【网站源码】
    <br>(全站模板)
    <br>https://github.com/technext

    Custom/sb-admin-2.js
    <br>Custom/sb-admin-2.min.css
    <br>https://www.bootcdn.cn/startbootstrap-sb-admin-2/
    <br>(这里面定义了 sidebar 相关的css样式)

1. 注意：一定要好好学会利用 div 以及 float:left 左悬浮标签！

---

## 参考教程

1. [Jinja2 for flask](http://jinja.pocoo.org/docs/2.10/templates/#synopsis)
2. [Bootstrap4 中文文档](http://bs4.ntp.org.cn/)

---

## 其他链接

1. [如何掌握所有的程序语言](http://www.yinwang.org/blog-cn/2017/07/06/master-pl)

