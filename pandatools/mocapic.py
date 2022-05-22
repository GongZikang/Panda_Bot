import json
import random
import requests
from nonebot.exceptions import CQHttpError
from hoshino import Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter
import urllib.request

_max = 10
EXCEED_NOTICE = f'您今天已经冲过{_max}次了，请明早5点后再来！'
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(5)

help_text = "=======来点老婆功能说明=======\n指令：来点[老婆名] / 多来点[老婆名]\n本功能使用mocabot网站资源，详情见：image.mocabot.cn/\n老婆库主要为BanGDream!企划声优，此外的高人气声优也收录了一些。"
sv = Service('来点老婆', manage_priv=priv.SUPERUSER, enable_on_default=False, visible=True, help_=help_text)

nick_name = {"227": ["厄厄漆"],
             "愛美": ["爱美", "cdd", "aimi"],
             "伊藤彩沙": ["卡比", "彩沙"],
             "遠藤ゆりか": ["有利息", "红发女人", "远藤祐里香"],
             "大橋彩香": ["大桥彩香", "hego", "大桥", "桥儿"],
             "前島亜美": ["前岛亚美", "amt", "amita", "亚美"],
             "上坂菫": ["政委", "同志", "上坂堇"],
             "中島由貴": ["中岛由贵", "由贵", "贵贵", "yuki", "yukki"],
             "伊藤美来": ["美来", "miku"],
             "明坂聡美": ["明坂聪美", "小明"],
             "進藤天音": ["进藤天音", "天音", "音宝", "妹妹"],
             "佐倉綾音": ["佐仓绫音", "佐仓", "樱小姐"],
             "相羽あいな": ["相羽爱奈", "aiai", "i83"],
             "Liyuu": ["liyuu", "鲤鱼"],
             "小仓唯": ["xcw"],
             "小原莉子": ["栗子", "莉子"],
             "志崎樺音": ["志崎桦音", "non", "non酱", "大小姐"],
             "西尾夕香": ["yuuka", "热水酱", "夕香"],
             "倉岡水巴": ["仓冈水巴"],
             "倉知玲鳳": ["仓知玲凤", "reo"],
             "赤尾ひかる": ["赤尾光"],
             "大西亜玖璃": ["大西亚玖璃"],
             "大塚紗英": ["大冢纱英", "sae", "番长"],
             "帆風千春": ["帆风千春", "千春"],
             "反田葉月": ["反田叶月", "反田"],
             "紡木吏佐": ["纺木吏佐", "tmtm", "tsumu", "牙白"],
             "逢田梨香子": ["逢田"],
             "富田麻帆": ["麻帆", "maho"],
             "岡田夢以": ["冈田梦以"],
             "高槻かなこ": ["高槻加奈子", "kanako"],
             "高橋李依": ["高桥李依", "李依李"],
             "高辻麗": ["高辻丽"],
             "各務華梨": ["各务华梨"],
             "根岸愛": ["根岸爱"],
             "工藤晴香": ["kdhr"],
             "鬼頭明里": ["鬼头明里"],
             "和氣あず未": ["和气あず未", "和气杏未"],
             "河瀬詩": ["河濑诗"],
             "黒沢ともよ": ["黑泽朋世"],
             "岬なこ": ["岬奈子"],
             "降幡愛": ["降幡爱"],
             "久保田未夢": ["久保田未梦"],
             "豊田萌絵": ["丰田萌绘"],
             "鈴木愛奈": ["铃木爱奈"],
             "楠木ともり": ["楠木灯"],
             "平嶋夏海": ["平岛夏海"],
             "斉藤朱夏": ["齐藤朱夏"],
             "青山なぎさ": ["青山渚"],
             "三村遙佳": ["三村遥佳"],
             "三森すずこ": ["三森铃子", "三森", "九木"],
             "三澤紗千香": ["三泽纱千香", "三泽", "氪金姬"],
             "上田麗奈": ["上田丽奈"],
             "生田輝": ["生田辉"],
             "水瀬いのり": ["水濑祈"],
             "西本里美": ["里美", "李美丽"],
             "相良茉優": ["相良茉优"],
             "小宮有紗": ["小宫有纱"],
             "小林愛香": ["小林爱香"],
             "小澤亜李": ["小泽亚李"],
             "星守紗凪": ["星守纱凪"],
             "岩田陽葵": ["岩田阳葵"],
             "葉月ひまり": ["叶月ひまり"],
             "伊波杏樹": ["伊波杏树"],
             "伊達さゆり": ["伊达小百合"],
             "櫻川めぐ": ["樱川めぐ", "樱川惠", "megu"],
             "種田梨沙": ["种田梨沙"],
             "諏訪七香": ["诹访七香"],
             "佐々木未来": ["佐佐木未来"]
             }


# 防止和HoshinoBot自带的setu模块冲突
@sv.on_rex(r"^(?:来点)([^色图]+)(?!色图)$")
async def mocapic(bot, ev):
    """随机叫一份老婆图，对每个用户有冷却时间"""
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ev, '您冲得太快了，请稍候再冲', at_sender=True)
        return

    _flmt.start_cd(uid)
    _nlmt.increase(uid)
    dataUrl = 'https://image.mocabot.cn/data/images.json'
    wifedata = json.loads(requests.get(dataUrl).text)
    wife_name = ev['match'].group(1)
    for i in nick_name.keys():
        for j in nick_name[i]:
            if wife_name == j:
                wife_name = i
                break

    sv.logger.info(f"得到的老婆名字为" + wife_name)
    if wife_name == '' or wife_name == '老婆' or wife_name == '随机老婆':
        wife_name = random.choice(list(wifedata.keys()))
        await bot.send(ev, "随机获得的老婆名字为" + wife_name, at_sender=True)
    if not (wife_name in wifedata):
        await bot.send(ev, '抱歉，我还不认识您老婆', at_sender=True)
        return
    name_encode = urllib.request.quote(wife_name, safe='/:?=&', encoding='utf-8')
    url_encode = 'https://image.mocabot.cn/data/imgs/' + name_encode + '.json'
    the_wife_data = json.loads(requests.get(url_encode).text)['files']
    pic_id = random.choice(the_wife_data)
    pic_url = 'https://acc.mocabot.cn/img.php?mode=file&name=' + name_encode + '&file=' + pic_id
    pic = f"[CQ:image,file={pic_url}]"

    try:
        await bot.send(ev, pic)
    except CQHttpError:
        sv.logger.error(f"发送图片{pic.path}失败")
        try:
            await bot.send(ev, '老婆图发送失败嘞...')
        except:
            pass


@sv.on_rex(r"(?:多来点)([^色图]+)(?!色图)$")
async def trimocapic(bot, ev):
    """随机叫三份老婆图，对每个用户有冷却时间"""
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ev, '您冲得太快了，请稍候再冲', at_sender=True)
        return

    _flmt.start_cd(uid)
    _nlmt.increase(uid)
    dataUrl = 'https://image.mocabot.cn/data/images.json'
    wifedata = json.loads(requests.get(dataUrl).text)
    wife_name = ev['match'].group(1)
    for i in nick_name.keys():
        for j in nick_name[i]:
            if wife_name == j:
                wife_name = i
                break

    sv.logger.info(f"得到的老婆名字为" + wife_name)
    if wife_name == '' or wife_name == '老婆' or wife_name == '随机老婆':
        wife_name = random.choice(list(wifedata.keys()))
        await bot.send(ev, "随机获得的老婆名字为" + wife_name, at_sender=True)
    if not (wife_name in wifedata):
        await bot.send(ev, '抱歉，我还不认识您老婆', at_sender=True)
        return
    name_encode = urllib.request.quote(wife_name, safe='/:?=&', encoding='utf-8')
    url_encode = 'https://image.mocabot.cn/data/imgs/' + name_encode + '.json'
    the_wife_data = json.loads(requests.get(url_encode).text)['files']
    random.shuffle(the_wife_data)
    pic_list = []
    mes_list = []
    for i in range(0, 3):
        pic_id = the_wife_data[i]
        pic_url = 'https://acc.mocabot.cn/img.php?mode=file&name=' + name_encode + '&file=' + pic_id
        pic = f"[CQ:image,file={pic_url}]"
        pic_list.append(pic)

    for img in pic_list:
        data = {
            "type": "node",
            "data": {
                "name": "DD机器人",
                "uin": "1145141919",
                "content": img
            }
        }
        mes_list.append(data)

    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)
