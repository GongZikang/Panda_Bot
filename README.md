# Panda_Bot
基于nonebot和HoshinoBot的Q群机器人插件

## 安装与部署

#### 首先你需要正确安装并运行HoshinoBot
关于HoshinoBot的详情见https://github.com/Ice-Cirno/HoshinoBot

确保您的Q群机器人已经能够正常运行，对于HoshinoBot相关的安装部署问题请在其页面寻找解决方案。

#### 安装本插件
可以直接用git clone或者在浏览器上下载本项目代码。

将pandatools整个文件夹及其文件放入HoshinoBot\hoshino\modules目录下。

把HoshinoBot\hoshino\config下的__bot__.py打开，MODULES_ON中添加一项'pandatools'并保存。

重启HoshinoBot


## 功能说明
### 1.saucenao识图功能 【本功能默认关闭】
#### 指令：
识图+空格+需要识别的图片<br />
或者发送识图后，机器人说明等待接收图片后再发送需要识别的图片。<br />
可使用“帮助识图”，获得机器人对该功能的说明。<br />
#### PS：
想要获得较好的识别结果，需要完整的插画或者完整的一页本子。<br />
对于残缺或者有额外黑边等的截图，结果非常糟糕。一般而言，相似度70以下的结果已经约等于失败了。<br />
<br />
<font color=Red>注意：</font>该功能需要填入saucenao的key。<br />
请于https://saucenao.com/完成注册<br />
打开https://saucenao.com/user.php?page=search-api<br />
找到api key一行，把后面的一串字符填入seachpic.py中的sauce_api = ""双引号之中<br />
本功能默认关闭，请在需要打开本功能的群内发送开启+空格+识图

### 2.搜索动漫图片
#### 指令：
搜图+角色名等<br />
来源为anime-pictures.net网站，使用该功能请确保服务器能与该网站连接顺利，必要时使用梯子。<br />
此网站的图片为SFW，不会出现漏点等问题，但几乎无法识别汉字，偶尔成功是因为识别为日文角色汉字名称。<br />
使用时还请使用角色的官方英文名称。<br />

例如：搜图ganyu<br />

Bot会发送对应图片一张<br />

### 3.来一张声优照片 【本功能默认关闭】
#### 指令：
##### 来点【声优名】

例如：来点伊藤彩沙

就会获得伊藤彩沙的随机图片

##### 多来点【声优名】

例如：多来点进藤天音

Bot会以合并形式发送对应图片三张

#### 昵称关键字说明

LP们的别称均写入在.py文件中的nick_name字典中。

~~由于本人不够D~~，并没有实现丰富的昵称，建议发送全称呼唤LP。

如果有想要被识别的昵称可以自行添加。

**<font color=Red>注意！</font>在实际使用中发现即便QQ发送繁体字，插件接收到的也是对应简体，若人名中有繁体字，一定要设置对应的简体昵称。**<br />
另外：在实际使用中发现群友更容易使用来点+动漫角色的方式呼唤setu，而setu功能确实是HoshinoBot自带的，为了避免混淆请斟酌是否要与此功能一同打开。<br />
代码里已经做了初步筛选，如果是来点【角色】色图，可以正确调用setu功能，而没有色图二字则为声优图片。<br />
本插件使用的图片来源均为 https://image.mocabot.cn/ <br />
非常感谢mocaBot的开发者准备了这样一份~~DD~~宝库


## 致谢


感谢[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)项目提供了非常便利的基础功能。
