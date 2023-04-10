# ops-edm

### 背景

ops-edm系统解决的是什么鬼？

Infrastructure的每月月报制作完成后，都是手动发送邮件，而且邮件没有格式，发出去的内容格式不太好看，所以使用ops-edm系统进行自动发送，自动调整格式和样式。

### 使用

#### 1.安装

~~~bash
pip3 install -r requirements.txt
~~~

#### 2.编写模板

将需要发送的内容填充到osinfra_monthly_template.xlsx

#### 3.编写edm.yaml文件

~~~bash
email_server_address: 'lists.osinfra.cn'   # mta的服务器地址
email_server_port: 465					   # mta的服务器端口
email_login_username: '***'				   # mta的登录用户
email_login_pwd: '***'					   # mta的登录密码
email_from_email: 'infra@lists.osinfra.cn' # 发送的邮箱地址
email_from_name: 'infra'				   # 发送的邮箱名称
email_subject: '基础设施运维月报'             # 发送的邮箱主题
email_sender_email:                        # 接收人的的邮箱
  - abc@qq.com
  - abc@163.com
~~~

### 4.执行

~~~bash
python3 edm.py
~~~



