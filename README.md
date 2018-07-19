# Webchat
project webchat and bbs

### 运行环境
    django 1.9.5   pymysql   mysql

### 运行方法
    1.  进入mysql创建数据库 day20_s12bbs
        create database day20_s12bbs;
    2. 创建表单
        python3 manage.py migrate 
    3. 创建超级用户
        python3 manage.py createsuperuser
        输入用户名和密码
    4. 进入 admin 管理界面创建 板块 
    
    5. 运行
        python3 manage.py runserver
        
        
