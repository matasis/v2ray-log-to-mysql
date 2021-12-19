# v2ray log to mysql

本项目用于将[v2ray-core](https://github.com/v2fly/v2ray-core) server端的日志导入到mysql方便查询和管理

### 将v2ray生成的access.log (如下结构)

```
2021/12/19 03:54:09 tcp:xxx.xxx.xxx.xxx:0 accepted tcp:alive.github.com:443 email: xxx@yyy.com
2021/12/19 03:57:04 tcp:xxx.xxx.xxx.xxx:0 accepted tcp:api.github.com:443 email: xxx@yyy.com
2021/12/19 03:59:29 tcp:xxx.xxx.xxx.xxx:0 accepted tcp:api.github.com:443 email: xxx@yyy.com
2021/12/19 03:59:44 tcp:xxx.xxx.xxx.xxx:0 accepted tcp:github.com:443 email: xxx@yyy.com
```

### 导入mysql数据库

|rdate|rtime|from_protocol|from_ip|from_port|state|target_protocol|target|target_port|user|
|----|----|----|----|----|----|----|----|----|----|
|2021-12-19|03:54:09|tcp|xxx.xxx.xxx.xxx|0|accepted|tcp|alive.github.com|443|xxx@yyy.com|
|2021-12-19|03:57:04|tcp|xxx.xxx.xxx.xxx|0|accepted|tcp|api.github.com|443|xxx@yyy.com|
|2021-12-19|03:59:29|tcp|xxx.xxx.xxx.xxx|0|accepted|tcp|api.github.com|443|xxx@yyy.com|
|2021-12-19|03:59:44|tcp|xxx.xxx.xxx.xxx|0|accepted|tcp|github.com|443|xxx@yyy.com|

>第一次使用先编辑config.ini
>安装python依赖:
```
pip install -r requirements.txt
```
>运行:
```
python main.py
```
