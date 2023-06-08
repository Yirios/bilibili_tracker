# bilibili_tracker

**<center>写在前面：这是一个数据库课程的大作业，现在由于bilibili-api-python库有些问题无法运行</center>**

## 一些准备与使用方法

1. python
   用到的第三方库
   ```powershell
   pip3 install bilibili-api-python
   pip3 install PyMySQL
   pip3 install requests 
   ``` 
   将 Credential.json 中的前五项填上。cookie 项直接复制即可，均可以在浏览器的开发者模式中找到。注意B站的 cookie 每天会刷新，在使用时最好更新一下 cookie。

2. MySQL
   将 Credential.json 中的后3项填上
   将 setdb.sql 中的sql语句直接粘贴到MySQL中

3. 运行
   在 main.py 的 get_mid()中写入需要录入数据库的UP主的uid，然后运行 main.py 即可

## python 爬虫部分
1. 获得UP主的视频列表
2. 爬取并写入视频信息（基本信息，弹幕，评论等）
3. 爬取并写入相关其他信息（分区，用户）
4. 定时更新数据
   
## MySQL 数据库部分

### 总E-R图
![Alt text](res/ERall.png)

### 常用查询
在 search.sql 中有一些常用的视图与查询可以直接复制使用

## 计划实现目标
1. 实现B站登录功能，可直接读取关注列表（已完成）
2. 利用WebUI实现交互
3. 解决B站cookie更新的问题
4. 简化准备过程
5. 提高爬虫效率与稳定性
