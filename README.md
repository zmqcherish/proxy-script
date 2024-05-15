# 脚本最新版 v0515.1
- 因Quan-X可能存在脚本更新延迟，根据你本地脚本第一行的version查看是否运行的是最新版
- 本项目不定期更新，如运行效果与预期不符，请确保脚本已更新到最新版。不排除脚本bug或第三方应用更新后与原有规则不匹配等可能
- 微博版本：14.5.0
- B站版本：7.26.0

# 说明
- 本项目用于自定义配置iOS系统上的App，主要针对微博去广告及其他自定义，和其他一些软件
- 使用前提：需到非大陆区AppStore下载Quantumult X / Surge
- Quan-X / Surge App本身付费，可自行网上找外区Apple ID免费下载，也可找各渠道付费购买
- Quan-X [不完全教程](https://www.notion.so/Quantumult-X-1d32ddc6e61c4892ad2ec5ea47f00917)


# 文件功能说明
## weibo_main.js & weibo_launch.js
> 可屏蔽微博app多数广告以及各部分推广模块
- 删除首页(tab1)流和超话中的广告、热推
- 删除视频号(tab2)流中的广告
- ~~删除发现页(tab3)轮播广告图~~
- 删除个人页(tab5)中的创作者中心下方的轮播图、为你推荐、用户任务和VIP一栏（可配置）
- 删除微博详情页的广告、相关推荐、微博主好物种草和关注博主模块（可配置）
- 删除微博开屏广告 | 参考[@yichahucha](https://github.com/yichahucha/surge/blob/master/wb_launch.js)
- 删除tab2菜单中的虚假通知
- 删除tab1顶部的签到和直播（可配置）
- 删除微博详情页菜单栏的新鲜事头像挂件等（可配置）
- 删除微博详情页评论区相关内容（可配置，默认关闭）
- 删除微博详情页评论区推荐内容（可配置，默认打开）
- 删除超话中可能感兴趣的超话、超话中的好友、超话好友关注、用户页可能感兴趣的人（可配置，默认关闭）
- 删除搜索结果页广告
- 将个人主页【关注】按钮默认值由【推荐】改为【关注的人】
- 自定义个人主页图标（可配置，默认关闭）[效果图](https://m.weibo.cn/2316757461/4693643559963746
)
- 关闭自动播放下一个视频（可配置，默认关闭）
- 删除微博详情页打赏模块（可配置，默认关闭）
- 自定义底部tab图标（可配置，默认关闭）[效果图](https://m.weibo.cn/2316757461/4695984200746208
)
- 【已删除】移除tab5新任务通知。[原样式](https://m.weibo.cn/2316757461/4696696879319087)
- 删除绿洲模块（可配置，默认关闭）
- 【待定】自定义开屏图片/视频。如有需求，可以考虑开发
- 删除个人页【让红包飞】模块
- 【03.12更新】新增屏蔽用户功能，如果有不得已需要关注的人（比如某些抽奖关注），但是又不想看TA的内容可以使用此配置。
- 【05.22更新】（重新）删除发现页(tab3)轮播广告图，需要配置weibo_config.js -> removeSearchWindow为true。其实轮播中有些不是广告，一起杀
- 【07.12更新】 删除消息页动态流的广告
- 【08.22更新】 删除超话tab页无关元素（可配置）
- 【08.23更新】 删除微博详情页超话新帖和新用户相关提示
- 【09.02更新】 删除初次打开搜索页的轮播图
- 【09.12更新】 修复超话无法签到bug
- 【10.11更新】 移除首页新版广告
- 【10.24更新】 移除用户页新版广告
- 【2023.03.21更新】 移除首页感兴趣的超话
- 【2024.05.15】移除转发流的广告和常看视频号更新
## weibo_config.js
> 微博自定义配置
- weibo_main.js文件中含有大量配置用于控制脚本的实际运行结果，如是否移除顶部直播或评论区相关内容等。如果不需要有自己的配置，可忽略此部分说明。
- 如果设置过自定义配置，对后续新增加的功能，如果不生效需要重新设置一次自定义配置。
- 如果需要有自己的特别需求，以评论区相关内容为例，默认是关闭(false)，即不移除。如果需要移除可复制[weibo_config.js](https://github.com/zmqcherish/proxy-script/blob/main/weibo_config.js)文件，然后修改 mainConfig.removeRelateItem = true 后，运行此文件即可。
- 屏蔽用户id获取方法：进入用户主页，选择复制链接，得到类似“https://weibo.com/u/xxx”的文本，xxx即为用户id。多个用户用英文逗号“,”分开
- 自定义个人主页图标设置：详见[微博皮肤.md](https://github.com/zmqcherish/proxy-script/blob/main/微博皮肤.md)
- 自定义底部tab图标：详见[底部tab.md](https://github.com/zmqcherish/proxy-script/blob/main/底部tab.md)
- Quan-X 运行方法1：在App中，点击【工具&分析】->【HTTP请求】页面上的右下角图标，在界面中粘贴上面的修改自定义值后的代码，然后点击运行（第一个图标）
- Quan-X 运行方法2（推荐）：可在配置文件中增加如下配置后，在【HTTP请求】页面上进一步编辑然后运行
```properties
[task_local]
0 0 23 1 * https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_config.js, tag=微博配置, img-url=https://raw.githubusercontent.com/zmqcherish/proxy-script/main/imgs/icon/weibo.png, enabled=false
```
- Surge 运行方法：在首页 -> 脚本 -> 编辑器，在界面中粘贴上面的修改自定义值后的代码，然后点击右下角执行

## bilibili.js
- 删除首页广告
- 删除首页竖版视频（可配置）

> B站自定义脚本文件
- 使用说明：[bilibili.md](https://github.com/zmqcherish/proxy-script/blob/main/bilibili/bilibili.md)



## weibo.conf
> Quan-X配置，微博订阅配置（下文Quan-X配置教程中使用）

## weibo.sgmodule
> Surge配置，微博订阅配置（下文Surge配置教程中使用）
## cherish.conf
> Quan-X配置，个人自用
- 知乎、微信公众号、B站去广告，均来自于网络
- 同weibo.conf功能相同的微博配置
- customize.js中的功能

## weibo_main.py
> Python 脚本，功能同weibo_main.js + weibo_launch.js，可用mitmproxy部署

# Quan-X 配置教程
1. 下载Quan-X App
2. 点击首页右下角风车按钮 -> MitM -> 生成证书
3. iPhone设置页 -> 通用 -> VPN与设备管理，找到Quantumult X开头的证书文件进行安装
4. iPhone设置页 -> 通用 -> 关于本机 -> 证书信任设置，打开Quantumult X开头的证书信任
5. 回到Quan-X App的MitM模块开关打开，重写模块开关打开
6. 在设置页最下方进入其他设置 -> VPN -> 始终开启
7. App中 -> 重写 -> 规则资源 -> 右上角添加，输入标签（任意名），资源路径填写 https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo.conf （或使用fast-conf）-> 右上角保存
8. 回到App首页顶部开启App运行即可


# Quan-X 文本模式配置
```properties
[rewrite_local]
# 微博去广告以及去除各部分推广模块
^https?://m?api\.weibo\.c(n|om)/2/(cardlist|searchall|page|messageflow|statuses/(unread_)?friends(/|_)timeline|groups/timeline|statuses/(container_timeline|unread_hot_timeline|extend|video_mixtimeline|repost_timeline)|profile/(me|container_timeline)|video/(community_tab|remind_info|tiny_stream_video_list)|checkin/show|\!/live/media_homelist|comments/build_comments|container/get_item|search/(finder|container_timeline|container_discover)) url script-response-body https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_main.js
# 删除微博开屏广告
^https?://(sdk|wb)app\.uve\.weibo\.com(/interface/sdk/sdkad.php|/wbapplua/wbpullad.lua) url script-response-body https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_launch.js
[mitm]
hostname = api.weibo.cn, mapi.weibo.com, *.uve.weibo.com
```


# Surge 配置教程
> 目前有bug，待修复
1. 下载Surge App
2. 首页 -> MitM -> 配置根证书 -> 生成新的CA证书 -> 安装证书
3. iPhone设置页 -> 通用 -> VPN与设备管理，找到Surge开头的证书文件进行安装
4. iPhone设置页 -> 通用 -> 关于本机 -> 证书信任设置，打开Surge开头的证书信任
5. 回到Surge App的MitM模块开关打开，Rewrite模块开关打开
6. 在更多页 -> 始终开启打开
7. 首页 -> 模块 -> 安装新模块 -> 路径填写 https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo.sgmodule
8. 安装模块后，进入首页左上角（Default）的外部资源中可以看到两个js文件
9. 回到App顶部开启App运行即可
10. [tip] 由于脚本不定期更新，安装的模块和外部资源需要左滑手动更新（暂未找到定时更新功能）

# Surge 文本模式配置
> 目前有bug，待修复
```properties
[Script]
http-response ^https?://m?api\.weibo\.c(n|om)/2/(cardlist|searchall|page|messageflow|statuses/(unread_)?friends(/|_)timeline|groups/timeline|statuses/(container_timeline|unread_hot_timeline|extend|video_mixtimeline|repost_timeline)|profile/(me|container_timeline)|video/(community_tab|remind_info|tiny_stream_video_list)|checkin/show|\!/live/media_homelist|comments/build_comments|container/get_item|search/(finder|container_timeline|container_discover)) requires-body=1,script-path=https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_main.js
http-response ^https?://(sdk|wb)app\.uve\.weibo\.com(/interface/sdk/sdkad.php|/wbapplua/wbpullad.lua) requires-body=1,script-path=https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_launch.js
[MITM]
hostname = %APPEND% api.weibo.cn, mapi.weibo.com, *.uve.weibo.com
```

# Contact me
- weibo:[@甄星cherish](https://weibo.com/zmqcherish)
# 免责声明
- 此脚本仅用于学习研究，不保证其合法性、准确性、有效性，请根据情况自行判断，本人对此不承担任何保证责任。
- 请勿将此脚本用于任何商业或非法目的，若违反规定请自行对此负责。

# 感谢
- [fastgit](https://doc.fastgit.org/)
- [@NobyDa](https://github.com/NobyDa)
- [@yichahucha](https://github.com/yichahucha)
- [@AirPods2](https://weibo.com/u/5750747182)
- [@chouchoui](https://github.com/chouchoui)
# 赞赏
![alt 赞赏码](https://raw.githubusercontent.com/zmqcherish/proxy-script/main/imgs/zsm3.jpg)