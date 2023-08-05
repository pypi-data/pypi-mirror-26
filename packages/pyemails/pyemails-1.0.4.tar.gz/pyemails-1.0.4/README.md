快速预览
* from pyemails import Email
* \# 申明用户名和密码及host, 腾讯企业邮箱：smtp.exmail.qq.com；需要设置 host='smtp.exmail.qq.com'
* email_obj = Email(user='example@qq.com', password='example', host='xxx')
* print email_obj.user,email_obj.password,email_obj.host
* \# \>\>\> example@qq.com, example, xxx
* \# 修改 host 
* email_obj.set_host(host='smtp.exmail.qq.com')
* print email_obj.user,email_obj.password,email_obj.host
* \#  \>\>\> example@qq.com, example, smtp.exmail.qq.com
* \# 发送内容
* email_obj.add_mime_text(u'你好')
* print email_obj.text
* \#  \>\>\> \<!DOCTYPE html\>\<html lang="en"\>\<body\>\<div\>你好\</div\>\</body\>\</html\>
* \# 添加文件
* email_obj.add_mime_file(r'D:\tmp\111.xlsx')
* \# 添加图片到正文
* email_obj.add_mine_image(image_path_list,table_name='title')
* email_obj.send(to_addrs=['tocom', ],cc=['cc@com', ], subject=subject)


