# 说明

- 目前仅支持iOS端（Android方法应该更多，暂无设备测试）
- 需到非大陆区AppStore下载Quantumult X / Surge
- Quan-X / Surge App本身付费，可自行网上找外区Apple ID免费下载
- 本项目不提供下载账号。share一个网上的[链接](https://id1314.com/?p=45)，不保证可用
- Quan-X [不完全教程](https://www.notion.so/Quantumult-X-1d32ddc6e61c4892ad2ec5ea47f00917)
# About Files

## weibo_main.js & weibo_launch.js
> 可屏蔽微博app多数广告以及各部分推广模块（不定期更新）
- 删除首页(tab1)流和超话中的广告、热推
- 删除视频号(tab2)流中的广告
- 删除发现页(tab3)轮播广告图
- 删除个人页(tab5)中的创作者中心下方的轮播图、为你推荐、用户任务和头像旁边的VIP icon（可配置）
- 删除微博详情页的广告、相关推荐、微博主好物种草和关注博主模块（可配置）
- 删除微博开屏广告 | 参考[@yichahucha](https://github.com/yichahucha/surge/blob/master/wb_launch.js)
- 删除tab2菜单中的虚假通知
- 删除tab1顶部的签到和直播（可配置）
- 删除微博详情页菜单栏的新鲜事头像挂件等（可配置）
- 删除微博详情页评论区相关内容（可配置，默认关闭）
- 删除超话中可能感兴趣的超话、超话中的好友、超话好友关注、用户页可能感兴趣的人（可配置，默认关闭）
- [10.17 update] 删除搜索结果页广告
- [10.17 update] 将个人主页【关注】按钮默认值由【推荐】改为【关注的人】
- [10.18 update] 自定义个人主页图标（测试中）
> 关于自定义配置（进阶使用）
- weibo_main.js文件中含有大量配置用于控制脚本的实际运行结果，如是否移除顶部直播或评论区相关内容等。如果不需要有自己的配置，可忽略此部分说明。
- 如果需要有自己的特别需求，以评论区相关内容为例，默认是关闭(false)，即不移除。如果需要移除可复制[weibo_config.js](https://github.com/zmqcherish/proxy-script/blob/main/weibo_config.js)文件，然后修改 mainConfig.removeRelateItem = true 后，运行此文件即可。
- 运行方法：在Quan-X App中，点击【构造HTTP请求】页面上的右下角图标，在界面中粘贴上面的修改自定义值后的代码，然后点击运行（第一个图标） 
> For Quan-X
```properties
[rewrite_local]
# 微博去广告以及去除各部分推广模块
^https?://m?api\.weibo\.c(n|om)/2/(cardlist|searchall|page|statuses/(unread_)?friends(/|_)timeline|groups/timeline|statuses/(unread_hot_timeline|extend)|profile/(me|statuses)|video/(community_tab|remind_info)|checkin/show|\!/live/media_homelist|comments/build_comments|container/get_item) url script-response-body https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_main.js
# 删除微博开屏广告
^https?://(sdk|wb)app\.uve\.weibo\.com(/interface/sdk/sdkad.php|/wbapplua/wbpullad.lua) url script-response-body https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_launch.js
[mitm]
hostname = api.weibo.cn, mapi.weibo.com, *.uve.weibo.com
```

> For Surge (手机上无surge无法测试，或许有人能帮忙吗)
```properties
[Script]
http-response ^https?://m?api\.weibo\.c(n|om)/2/(cardlist|searchall|page|statuses/(unread_)?friends(/|_)timeline|groups/timeline|statuses/(unread_hot_timeline|extend)|profile/(me|statuses)|video/(community_tab|remind_info)|checkin/show|\!/live/media_homelist|comments/build_comments|container/get_item) requires-body=1,script-path=https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_main.js
http-response ^https?://(sdk|wb)app\.uve\.weibo\.com(/interface/sdk/sdkad.php|/wbapplua/wbpullad.lua) requires-body=1,script-path=https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_launch.js
[MITM]
hostname = api.weibo.cn, mapi.weibo.com, *.uve.weibo.com
```
## weibo.conf
> Quan-X配置，微博订阅配置（简单配置教程中使用）
## cherish.conf
> Quan-X配置，个人常用配置，包括知乎、微信公众号、B站去广告，均来自于网络，最后一部分为上文的微博配置

## weibo_main.py
> Python 脚本，功能同weibo_main.js + weibo_launch.js，可用mitmproxy部署

# Quan-X 简单配置教程
1. 下载Quan-X App
2. 点击首页右下角风车按钮 -> MitM -> 生成证书
3. iPhone设置页 -> 通用 -> 描述文件与设备管理，找到Quantumult X开头的证书文件进行安装
4. iPhone设置页 -> 通用 -> 关于本机 -> 证书信任设置，打开Quantumult X开头的证书信任
5. 回到Quan-X App的MitM模块开关打开，重写模块开关打开
6. 在设置页最下方进入其他设置 -> VPN -> 始终开启
7. 在重写模块 -> 引用 -> 右上角添加，输入标签（任意名），资源路径填写 https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo.conf -> 右上角保存
8. 回到App首页顶部开启App运行即可

# Contact me
weibo:[@甄星cherish](https://weibo.com/zmqcherish)

# 免责声明
- 此脚本仅用于学习研究，不保证其合法性、准确性、有效性，请根据情况自行判断，本人对此不承担任何保证责任。
- 请勿将此脚本用于任何商业或非法目的，若违反规定请自行对此负责。
