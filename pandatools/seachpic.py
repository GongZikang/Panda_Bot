# 此功能需要额外安装saucenao_api
# 可用pip install -U saucenao_api指令安装

import time
from hoshino import Service, priv
from saucenao_api import *
from hoshino.util import FreqLimiter, DailyNumberLimiter
from nonebot.command.argfilter import extractors, controllers


help_text = '======识图功能使用说明======\n使用命令为：识图+空格+图片\n或者发送识图指令后挨着发送需要识别的图片\n本功能在识别完整插画或者完整一页本子时表现较好，其余情况就不要抱有太大期待了。'
sv = Service('识图', visible=True, manage_priv=priv.SUPERUSER, enable_on_default=False, help_=help_text)
_max = 5
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(15)
EXCEED_NOTICE = f'您今天已经查询过过{_max}次了，请明早5点后再来！'

# 下面填入saucenao的api
sauce_api = ""


@sv.on_command('以图搜图', aliases=('识图', '搜索图片'))
async def searchpic(session):
    ev = session.event
    bot = session.bot
    uid = str(ev['user_id'])

    if not _nlmt.check(uid):
        await session.send(EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await session.send('请求过快，请稍等片刻~', at_sender=True)
        return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)
    # 若发送识图+空格+图片可以直接获取图片
    piclist = session.current_arg_images
    print(piclist)
    # 仅发送识图（如手机端），未能获得图片，则等待下一条消息接收到图片
    if len(piclist) == 0:
        piclist = await session.aget('pic', prompt='请发送需要识别的图片', arg_filters=[extractors.extract_image_urls, controllers.handle_cancellation(session)], at_sender=True)
    if len(piclist) == 0:
        session.finish('未识别到图片,请发送图片以识别,详细说明请发送[帮助识图]', at_sender=True)
    await bot.send(ev, "已接收图片，正在分析中……请稍等……", at_sender=True)
    sauce = SauceNao(sauce_api)
    pic = piclist[0]
    try:
        res = sauce.from_url(pic)
    except SauceNaoApiError:
        sv.logger.error(f"查询失败SauceNaoApiError")
        try:
            await bot.send(ev, '啊呀，电波被劫持，查询失败...')
        except:
            pass
    if not res:
        await session.finish(f'识别失败,请稍后再试', at_sender=True)
        return
    pic_list = []
    for i in res:
        # 结果按照相似度排列，当发现一条结果相似度低于50，相关性渺茫，忽略。不过至少保留一条结果。
        # 查询结果中并非每项都有标题、作者、链接等信息，需要做判断。
        if i.similarity < 50 and len(pic_list) > 0:
            pic_list.append('此匹配相似度过低，已忽略。')
            break
        if i.similarity:
            info = '相似度:' + str(i.similarity) + '%\n'
        if i.title:
            info = info + '标题:「' + i.title.replace(',', '，').replace('[', '【').replace(']', '】') + '」\n'
        if i.author:
            info = info + '作者:「' + i.author.replace(',', '，').replace('[', '【').replace(']', '】') + '」\n'

        if len(i.urls) >= 1:
            info = info + '图片地址:「' + i.urls[0] + '」\n'
        pic_list.append(f'[CQ:text,text={info}]')
        pic_list.append(f'[CQ:image,cache=0,file={i.thumbnail}]')

    mes_list = []
    for img in pic_list:
        data = {
            "type": "node",
            "data": {
                "name": "PandaBot-识图",
                "uin": "1145141919",
                "content": img
            }
        }
        mes_list.append(data)

    print(mes_list)
    try:
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)
    except:
        # 实际使用中多次出现send_group_forward_msg在go-cqhttp处判定为格式有误无法发送，怀疑,[]符号，但做了转换后还是会出现。
        # 暂时没有找到确切的原因，所以出现错误后转换成多条普通消息发送。
        await session.send("合并转发出现未知错误，改为多条普通消息。")
        for img in pic_list:
            await session.send(img)
            time.sleep(0.2)
    session.finish('以上就是您的识图结果啦~', at_sender=True)


