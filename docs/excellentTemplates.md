## 优秀网站模板

* Start Bootstrap (SB-admin) 模板
  <br>https://startbootstrap.com/templates/sb-admin/
 
## flask 部署

* Flask+uwsgi+Nginx+Ubuntu 部署
  <br>https://www.cnblogs.com/leiziv5/p/7137277.html
  
  ```
  pnf_project> cat pnf_project.ini
  [uwsgi]
  module = wsgi:app

  master = true
  processes = 8
  threads = 5

  socket = myproject.sock
  chmod-socket = 660
  vacuum = true

  die-on-term = true
  ```
