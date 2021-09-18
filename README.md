# About Files

## weibo_main.js
> Quan-X脚本，可屏蔽微博app多数广告以及个人中心的推广模块（不定期更新）
- 删除首页(tab1)流中的广告和热推
- 删除视频号(tab2)流中的广告
- 删除个人页(tab5)中的创作者中心下方的轮播图、为你推荐和头像旁边的VIP icon
```properties
[rewrite_local]
^https?://m?api\.weibo\.c(n|om)/2/(cardlist|page|statuses/(unread_)?friends(/|_)timeline|groups/timeline|statuses/unread_hot_timeline|profile/me|video/community_tab) url script-response-body https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_main.js

[mitm]
hostname = api.weibo.cn, mapi.weibo.com, *.uve.weibo.com
```
## cherish.conf
> Quan-X配置，个人常用配置，包括知乎、微信公众号、B站去广告，均来自于网络，最后一部分为上文的微博配置

## weibo_main.py
> Python 脚本，功能同weibo_main.js，可用mitmproxy部署



# Contact me
weibo:[@甄星cherish](https://weibo.com/zmqcherish)
