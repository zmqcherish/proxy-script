# 说明
- 截至2021.10.24，目前此功能仅支持微博**会员**。不排除后续突破会员限制可能
- 操作略微繁琐，效果图如下
- ![alt 效果图](https://wx4.sinaimg.cn/large/002wMSrPly1gvqvdxjs8jg60go09uhdu02.gif)

# 关闭方法
- 在weibo_config.js中设置tabIconVersion = 0，运行后即可关闭自定义皮肤

# 打开方法
1. 在微博app中进入会员中心 -> 个性皮肤，选择一个你喜欢的皮肤进行设置
2. 设置完成后，后台关闭微博app
3. 在weibo_config.js中设置tabIconVersion为大于100的任意数，每次需要更新皮肤时候设置为与上一次**不同值**即可。比如第一次tabIconVersion=101，第二次tabIconVersion=110
4. 在weibo_config.js中设置tabIconPath值未具体的皮肤文件路径，具体方法参考下文
5. 运行修改后的配置文件
6. 重新进入微博app，会提示“**您使用的皮肤已更新**”，点击更新即可。如果未弹出对话框，尝试重新退出再进入app


# 皮肤文件 - 准备
- 方法一：使用别人提供的zip文件，可忽略这一步
- 方法二：自定义，下载[示例皮肤](https://vip.storage.weibo.com/vip_lightskin/lightskin_79_1.0.zip)，然后解压后使用自己的图片替换文件夹中的图片（文件名不变），然后打包获得一个zip文件。其中，dropdown_lightskin.png为首页下拉对应的图片，tabbar_lightskin_1.png - tabbar_lightskin_5.png 为底部5个tab对应的图片，其他文件可忽略不做替换

# 皮肤文件 - 链接
- 方法一：使用别人提供的zip文件，获得一个xxx.zip链接
- 方法二：将自定义的zip文件上传到[七牛云](https://portal.qiniu.com/)的对象存储中，然后在文件详情中获取文件链接。上传步骤详见下文
- 方法三（不稳定）：将zip文件上传到自己的GitHub项目中获取对应的raw，此方法不稳定
- 方法四：需要大家集思广益，如有合适方法烦请告知[@甄星cherish](https://weibo.com/zmqcherish)


# 七牛云上传步骤
1. 注册[七牛云](https://www.qiniu.com/?cps_key=1hifrwd2d5ope)账号
2. 在[空间管理](https://portal.qiniu.com/kodo/bucket)中新建空间。每个空间对应域名有效期30天，过期后可再次创建新的空间已获取新的域名。
3. 在空间管理中找到新建的空间，进入**文件管理** -> **上传文件**，上传自定义zip文件
4. 在对应的文件**详情**中获取**文件链接**
