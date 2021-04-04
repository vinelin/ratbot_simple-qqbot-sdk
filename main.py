from qqbot import Bot,command_map
import requests,json,re,random
from configparser import ConfigParser
from postbody import *
from Imgdb import ImgUrlTable

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
    text = '直接打出文字命令,或者特定形式和文字命令\n命令与内容间用空格隔开\n'
    for k in command_map.keys():
        if re.findall('[CQ:at.*?]',k,re.S):
            text = text+str(i)+'.'+'调戏机器人或菜单，需要@机器人'+'\n'
            i = i+1
            continue
        text = text+str(i)+'.'+k+'\n'
        i = i+1
    return text


#一言功能
@bot.commands('说批话')
async def hitokoto(ctx:dict):
    result = requests.get('http://v1.hitokoto.cn?encode=json&charset=utf-8?').json()
    post_body = post_content(send_text(result['hitokoto']), send_emoji('298'))
    return await group_send(ctx.get('group_id'), post_body)
#自动回复和菜单功能，需要@机器人
@bot.commands(f"[CQ:at,qq={bot.env['bot_id']}]")
async def tulinreply(ctx:dict):
    try:
        content = ctx['comAndcont'][1]
        if content == '菜单':
            menu_text = await menu(command_map)
            post_body = post_content(send_text(menu_text))
            return await group_send(ctx.get('group_id'), post_body)
    except IndexError as e:
        return
    reply = requests.get(f'http://api.brhsm.cn/lt.php?msg={content}').json()["text"]
    post_body = post_content(send_at(ctx['sender_id']),send_text(reply))
    return await group_send(ctx.get('group_id'), post_body)
#添加图片[空格]图片 添加图片到群友图库
@bot.commands('添加图片')
async def add_image(ctx:dict):
    db = ImgUrlTable()
    try:
        url = re.search('url=(.*?)]', ctx['comAndcont'][1], re.S).group(1)
    except (IndexError,AttributeError) as e:
        post_body = post_content(send_text('没发图'))
        return await group_send(ctx.get('group_id'), post_body)
    db.add_row(url)
    del db
    post_body = post_content(send_text('添加成功！'))
    return await group_send(ctx.get('group_id'), post_body)
#群友图库 发送图库里的随机图片
@bot.commands('群友图库')
async def random_image(ctx:dict):
    db = ImgUrlTable()
    image_list = db.select_all()
    image_len = len(image_list)
    if image_len == 0:
        post_body = post_content(send_text('图库为空！'))
        return await group_send(ctx.get('group_id'), post_body)
    print(image_list)
    random_index = random.randint(0, image_len-1)
    del db
    post_body = post_content(send_image(image_list[random_index][1]))
    return await group_send(ctx.get('group_id'), post_body)

if __name__ == '__main__':

    bot.run()