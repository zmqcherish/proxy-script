# About Files

## weibo_main.js
> Quan-X脚本，可屏蔽微博app多数广告以及各部分推广模块（不定期更新）
- 删除首页(tab1)流中的广告和热推
- 删除视频号(tab2)流中的广告
- 删除发现页(tab3)轮播广告图
- 删除个人页(tab5)中的创作者中心下方的轮播图、为你推荐、用户任务和头像旁边的VIP icon（可配置）
- [09.22 update] 删除微博详情页的广告、相关推荐、微博主好物种草和关注博主模块（可配置）
- [09.23 update] 删除微博开屏广告 |参考@yichahucha 
- [09.23 update] 删除tab2菜单中的虚假通知（测试中）
- [09.24 update] 删除tab1顶部的签到和直播（可配置）
```properties
[rewrite_local]
# 微博去广告以及去除各部分推广模块
^https?://m?api\.weibo\.c(n|om)/2/(cardlist|page|statuses/(unread_)?friends(/|_)timeline|groups/timeline|statuses/(unread_hot_timeline|extend)|profile/me|video/(community_tab|remind_info)|checkin/show|\!/live/media_homelist) url script-response-body https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_main.js
# 删除微博开屏广告
^https?://(sdk|wb)app\.uve\.weibo\.com(/interface/sdk/sdkad.php|/wbapplua/wbpullad.lua) url script-response-body https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_launch.js
[mitm]
hostname = api.weibo.cn, mapi.weibo.com, *.uve.weibo.com
```
## cherish.conf
> Quan-X配置，个人常用配置，包括知乎、微信公众号、B站去广告，均来自于网络，最后一部分为上文的微博配置

## weibo_main.py
> Python 脚本，功能同weibo_main.js，可用mitmproxy部署



# Contact me
weibo:[@甄星cherish](https://weibo.com/zmqcherish)

# 免责声明
- 此脚本仅用于学习研究，不保证其合法性、准确性、有效性，请根据情况自行判断，本人对此不承担任何保证责任。
- 请勿将此脚本用于任何商业或非法目的，若违反规定请自行对此负责。
