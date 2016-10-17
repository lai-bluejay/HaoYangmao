
# 使用方法


1、请确保你已经安装 python2.7

2、
```python
git clone git@github.com:linjunzhu/smzdm_checkin_daily.git
cd smzdm_checking_daily
```

3、修改`account.ini`
```python
# 可以写多个，同时签到
[user1]
username=iamusername@gmail.com
password=iampassword
[user2]
username=iamusername@gmail.com
password=iampassword
```
4、
```python
python smzdm.py
```

此时登录「什么值得买」，你会看到已经签到成功了。

#每天自动执行
1、 确保你使用 Linux or Mac OSX 系统

2、
```shell
# 开始编辑自动执行脚本
crontab -e
```
```shell
# 在文件末尾添加（路径根据实际情况修改)
# 每天早上7点将进行签到
0 7 * * * /bin/sh /home/deployer/smzdm_checkin_daily/smzdm_execute.sh start
```
```shell
# 查看自动执行脚本
cdeployer@Xshare:~$ crontab -l
0 7 * * * /bin/sh /home/deployer/smzdm_checkin_daily/smzdm_execute.sh start
```
