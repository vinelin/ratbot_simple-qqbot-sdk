from typing import Optional,Dict,Any
from fastapi import FastAPI,Request
from pydantic import BaseModel
import uvicorn,json,requests,re
#使用FastAPI框架
app = FastAPI()
command_map = {}
#定义Bot类
class Bot:
    env = {}
    env['host'] = "127.0.0.1"
    env['port'] = 8000
    env['post_port'] = 5700
    env['bot_id'] = None
    @app.post('/')
    async def cqhttp_post(request: Request):
        request_json = await request.json()
        if request_json['post_type'] == 'message':
            print(request_json)
            #ctx 保存收到的信息
            ctx = {}
            #消息
            ctx['message'] = request_json['message']
            #未处理的消息
            ctx['raw_message'] = request_json['raw_message']
            #群号
            ctx['group_id'] = request_json['group_id']
            ctx['sender_id'] = request_json['sender']['user_id']
            # user_id = request_json['sender']['user_id']
            #命令和内容列表
            ctx['comAndcont'] = ctx['message'].split(' ', 1)
            print(ctx)
            if command_map.get(ctx['comAndcont'][0]):
                print(command_map)
                await command_map[ctx['comAndcont'][0]](ctx)
        return {'request_json': request_json}

    def run(self,host=env['host'],port=env['port']):
        uvicorn.run(app="qqbot:app",host=host, port=port, reload=True)

    #装饰器 将指定命令加入命令菜单
    def commands(self,command:str):
        def decorater(func):
            command_map[command] = func
        return decorater





if __name__ == '__main__':
    bot = Bot()
    bot.run()






