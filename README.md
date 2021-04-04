# 🐭老鼠人Bot
基于[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)和[FastAPI](https://fastapi.tiangolo.com/)的QQ机器人自用框架。

![ratbot_simple-qqbot-sdk](https://socialify.git.ci/vinelin/ratbot_simple-qqbot-sdk/image?font=KoHo&forks=1&owner=1&pattern=Plus&stargazers=1&theme=Dark)

# 使用方法
### 测试python版本：3.6.12

### 1.安装所需要的第三方库
```
pip install fastapi
pip install uvicorn[standard]
pip install requests
```
### 2.修改config.ini中的bot_id为机器人的QQ

### 3.参考[教程](https://docs.go-cqhttp.org/guide/quick_start.html#%E4%BD%BF%E7%94%A8)将go-cqhttp配置好并运行起来。
 特别注意将配置文件中的post_urls项需要配置到我们FastAPI运行的uvicorn服务器IP地址。
格式参考：post_urls: {
        "127.0.0.1:8000":secret
    }
    待续...
