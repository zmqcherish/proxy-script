# bilibili脚本使用说明

## 主要功能
- 删除首页广告
- 删除首页竖版视频（可配置，默认关闭）
- (目前删除不完备，某些情况可能无法删除，待进一步排查)

### 方法一（推荐）：直接使用 bilibili.conf 文件
- App中 -> 重写 -> 规则资源 -> 右上角添加，输入标签（任意名），资源路径填写 https://raw.githubusercontent.com/zmqcherish/proxy-script/main/bilibili/bilibili.conf -> 右上角保存

### 方法二：Quan-X 文本模式配置
```properties
[rewrite_local]
# bilibili脚本
^https://app.(biliapi|bilibili).(net|com)/x/v2/feed/index url script-response-body https://raw.githubusercontent.com/zmqcherish/proxy-script/main/bilibili/bilibili.js
[mitm]
hostname = app.biliapi.net, app.bilibili.com
```

### 如何删除竖版视频
	因每个人的需求不同，默认情况首页的竖版视频不会删除，如需要，可按下面方法操作

在 Quan-X App种增加如下配置后，在【工具&分析】->【HTTP请求】然后选择B站配置，右滑运行
```properties
[task_local]
0 0 23 1 * https://raw.githubusercontent.com/zmqcherish/proxy-script/main/bilibili/bilibili_config.js, tag=B站配置, img-url=https://raw.githubusercontent.com/zmqcherish/proxy-script/main/imgs/icon/bilibili.png, enabled=false
```