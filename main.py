from qqbot import Bot,command_map
import requests,json,re
from configparser import ConfigParser
bot = Bot()
config = ConfigParser()
config.read('config.ini', encoding="UTF-8")
bot.env['bot_id'] = config.get("config", "bot_id")
print(bot.env)
#发送私聊信息
# def person_send(user_id, post_body):
#     post_url = ''.join(['http://', bot.env['host'], ':', str(bot.env['post_port'])])
#     r = requests.post(post_url + '/send_private_msg?user_id=' + str(user_id),
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(post_body))
#     print(r.text)

#发送群聊信息函数
async def group_send(group_id, post_body: dict):
    post_url = ''.join(['http://', bot.env['host'], ':', str(bot.env['post_port'])])
    r = requests.post(post_url + '/send_group_msg?group_id=' + str(group_id),
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(post_body))
    print(r.text)
#菜单功能
async def menu(command_map:dict):
    i = 1
    text = ''
    for k in command_map.keys():
        if re.findall('[CQ:at.*?]',k,re.S):
            text = text+str(i)+'.'+'调戏机器人或菜单'+'\n'
            i = i+1
            continue
        text = text+str(i)+'.'+k+'\n'
        i = i+1
    return text


#一言功能
@bot.commands('说批话')
async def hitokoto(ctx:dict):
    result = requests.get('http://v1.hitokoto.cn?encode=json&charset=utf-8?').json()
    post_body = {
        "message": [
            {
                "type": "text",
                "data": {"text": result['hitokoto']}
            },
            {
                "type": "face",
                "data": {"id": "298"}
            },
            {
                "type": "text",
                "data": {"text": result['from']}
            }
        ]
    }
    return await group_send(ctx.get('group_id'), post_body)
#自动回复和菜单功能，需要@机器人
@bot.commands(f"[CQ:at,qq={bot.env['bot_id']}]")
async def tulinreply(ctx:dict):
    try:
        content = ctx['comAndcont'][1]
        if content == '菜单':
            menu_text = await menu(command_map)
            post_body = {
            "message": [
                {
                    "type": "text",
                    "data": {"text": menu_text}
                }
                ]
            }
            return await group_send(ctx.get('group_id'), post_body)
    except KeyError as e:
        return
    reply = requests.get(f'http://api.brhsm.cn/lt.php?msg={content}').json()["text"]
    post_body = {
        "message": [
            {
                "type": "at",
                "data": {
                    "qq": ctx['sender_id']
                }
            },
            {
                "type": "text",
                "data": {"text": reply}
            }
        ]
    }
    return await group_send(ctx.get('group_id'), post_body)

if __name__ == '__main__':

    bot.run()