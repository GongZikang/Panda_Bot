# 使用anime-pictures.net搜索动漫图片，使用前请确保服务器能与该网站正常连接。
from bs4 import BeautifulSoup
import requests
import re
import random
from hoshino import Service, priv
from nonebot.exceptions import CQHttpError
from hoshino.util import FreqLimiter, DailyNumberLimiter

_max = 8
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(25)
EXCEED_NOTICE = f'您今天已经冲过{_max}次了，请明早5点后再来！'

help_text = "====搜图使用说明====\n指令为：搜图[x]，x建议使用角色英文名，少量支持日文。\n本功能获取的是原图，数据量较大反应速度会比较慢。\nBot管理员可以使用补充营养[目标QQ号]重置次数。"
sv = Service('搜图', manage_priv=priv.SUPERUSER, enable_on_default=True, visible=True, help_=help_text)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76'
}


@sv.on_prefix('搜图')
async def soutu(bot, ev):
    uid = str(ev.sender['user_id'])
    if not _nlmt.check(uid):
        await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ev, '您冲得太快了，请稍候再冲', at_sender=True)
        return
    _flmt.start_cd(uid)
    char_name = str(ev.message)
    res = requests.get(
        'https://anime-pictures.net/pictures/view_posts/0?search_tag=' + char_name + '&order_by=rating&ldate=0&lang=zh_CN',
        headers=headers)
    soup = BeautifulSoup(res.text, features="lxml")
    num = soup.find(style="text-align: center;line-height: 16px;").text

    # 搜索到的图片数量
    num = re.match(r'(\d+) 张图片在提交', str(num)).group(1)

    # 按评分降序排列，取前三分之一
    num = int(num) // 3
    if num <= 1:
        await bot.send(ev, '啊这，没有搜到您想要的图片呢\n建议您搜索角色的英文名呢')
        return
    _nlmt.increase(uid)
    pic_num = random.randint(0, num - 1)

    # 一页80张图
    page_num = pic_num // 80
    pic_num = pic_num % 80
    # 若选择第0页之后，需要重新获取该页的内容
    if page_num > 0:
        res = requests.get(
            'https://anime-pictures.net/pictures/view_posts/' + str(
                page_num) + '?search_tag=' + char_name + '&order_by=rating&ldate=0&lang=zh_CN',
            headers=headers)
        soup = BeautifulSoup(res.text, features="lxml")
    pic_div = soup.find(class_="posts_block")
    pic_url = pic_div.find_all(name='a')
    pic_url_list = []
    for url in pic_url:
        pic_url_list.append(url.attrs['href'])
    pic_url_list = pic_url_list[::2]
    pic_name = pic_url_list[pic_num]
    await bot.send(ev, 'OK~正在获取图片中，请稍等……')
    pic_url = "https://anime-pictures.net" + pic_name
    res = requests.get(pic_url, headers=headers)
    soup = BeautifulSoup(res.text, features="lxml")
    target_div = soup.find(id='big_preview_cont')
    target_url = target_div.find(name='a').attrs['href']
    pic = f"[CQ:image,file=https://anime-pictures.net{target_url},c=3]"
    try:
        await bot.send(ev, pic)
    except CQHttpError:
        sv.logger.error(f"发送搜到的图片失败")
        try:
            await bot.send(ev, '啊呀，图图发送失败嘞...明明很健全的说...')
        except:
            pass


@sv.on_prefix('补充营养')
async def buchongyingyang(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.send(ev, "小孩子别想太多了，健康成长才能成为将来的栋梁。")
    else:
        uid = str(ev.message)
        _nlmt.count.clear()
        await bot.send(ev, f"营养已补充！{uid}现在又可以冲{_max}次，注意身体哦！")
