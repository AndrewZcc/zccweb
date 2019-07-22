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

1. **TODO**: 遗留问题：怎么用 lazypinyin 获取安全字符串？


1. python-flask项目 **端口设置无效**
    
    https://www.cnblogs.com/xiaodai0/p/10460751.html
    <br>（解决方案：用 python解释器 运行，使用生产环境[Production],而非默认的开发环境[Development]）
    
1. 当 8090端口 被占用时

    - 使用 `app.run(host='0.0.0.0', port='8090')` 不会报错，但 浏览器访问时 会报 `405 Not Allowed` 错误；
    - 建议 首次运行新项目用 `app.run(host='127.0.0.1', port='8090')` 先尝试运行，如果该端口已被占用，使用该命令会提供报错信息！


1. 如何让sidebar左侧边栏导航在垂直方向全尺寸拉伸？

    https://blog.csdn.net/qq_35393869/article/details/88043093
    
    ```css
    ✖️height: calc(100% - 10px);
    ✔️height: calc(100vh - 48px);
    ```

1. 注意：一定要好好学会利用 div 以及 float:left 左悬浮标签！

---

## 参考教程

1. [Jinja2 for flask](http://jinja.pocoo.org/docs/2.10/templates/#synopsis)
2. [Bootstrap4 中文文档](http://bs4.ntp.org.cn/)
