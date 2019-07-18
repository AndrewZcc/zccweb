## 所遇问题列表

1. python-flask项目 **端口设置无效**
    
    https://www.cnblogs.com/xiaodai0/p/10460751.html
    <br>（解决方案：用 python解释器 运行，使用生产环境[Production],而非默认的开发环境[Development]）
    
2. 当 8090端口 被占用时

    - 使用 `app.run(host='0.0.0.0', port='8090')` 不会报错，但 浏览器访问时 会报 `405 Not Allowed` 错误；
    - 建议 首次运行新项目用 `app.run(host='127.0.0.1', port='8090')` 先尝试运行，如果该端口已被占用，使用该命令会提供报错信息！


---

## 参考教程

1. [Jinja2 for flask](http://jinja.pocoo.org/docs/2.10/templates/#synopsis)
2. [Bootstrap4 中文文档](http://bs4.ntp.org.cn/)
