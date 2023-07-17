#pip install mitmproxy==6.0.2
# https://www.mitmproxy.org/downloads
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from util import *

#微博详情页配置
main_config = {
	'removeRelate': True,	#相关推荐
	'removeGood': True,		#微博主好物种草
	'removeFollow': True,	#关注博主
	'removeRelateItem': True,	#评论区相关内容
	'removeRecommendItem': True,	#评论区推荐内容
	'removeSearchWindow' : True,	#搜索页滑动窗口
	'profileSkin1': ["https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaingvoj6046046dg802.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaiuoxtj6046046dga02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaiytuyj60460463yv02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaj19hvj6046046aac02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaj5ka0j6046046jrp02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaj9jfmj6046046dg502.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajd0hfj60460463yu02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajfce5j6046046wet02.jpg"],
	'profileSkin2': ["https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajhmrnj6046046jro02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajmgs0j60460460t102.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajp9uuj6046046jrp02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajrwrwj6046046dg102.jpg"],
	'tabIconVersion': 11,
	'tabIconPath': 'http://5b0988e595225.cdn.sohucs.com/skin-hebe.zip',
}

# 'profileSkin1': ['https://h5.sinaimg.cn/upload/1071/632/2019/01/11/Fat4_tabbar_lightskin_2.png', 'https://h5.sinaimg.cn/upload/108/914/2018/11/26/mario_tabbar_lightskin_1.png', 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png', 'https://h5.sinaimg.cn/upload/1071/632/2018/11/06/zhangcaoyantuanzi_tabbar_lighskin_4.png', 'https://h5.sinaimg.cn/upload/1071/632/2019/01/11/Fat4_tabbar_lightskin_4.png', 'https://h5.sinaimg.cn/upload/108/914/2018/11/26/mario_tabbar_lightskin_3.png', 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_4.png', 'https://wx1.sinaimg.cn/large/006Y6guWly1gvjc93r3yzj605k05kjs102.jpg'],
# 'profileSkin2': ['https://h5.sinaimg.cn/upload/1071/632/2019/01/11/Fat4_tabbar_lightskin_1.png', 'https://h5.sinaimg.cn/upload/108/914/2018/11/26/mario_tabbar_lightskin_5.png', 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_3.png', 'https://h5.sinaimg.cn/upload/1071/632/2018/11/06/zhangcaoyantuanzi_tabbar_lighskin_5.png']

item_menus_config = {
	'creator_task':False,					#转发任务
	'mblog_menus_custom':False,				#寄微博
	'mblog_menus_video_later':True,			#可能是稍后再看？没出现过
	'mblog_menus_comment_manager':True,		#评论管理
	'mblog_menus_avatar_widget':False,		#头像挂件
	'mblog_menus_card_bg': False,			#卡片背景
	'mblog_menus_long_picture':True,		#生成长图
	'mblog_menus_delete':True,				#删除
	'mblog_menus_edit':True,				#编辑
	'mblog_menus_edit_history':True,		#编辑记录
	'mblog_menus_edit_video':True,			#编辑视频
	'mblog_menus_sticking':True,			#置顶
	'mblog_menus_open_reward':True,			#赞赏
	'mblog_menus_novelty':False,			#新鲜事投稿
	'mblog_menus_favorite':True,			#收藏
	'mblog_menus_promote':True,				#推广
	'mblog_menus_modify_visible':True,		#设置分享范围
	'mblog_menus_copy_url':True,			#复制链接
	'mblog_menus_follow':True,				#关注
	'mblog_menus_video_feedback':True,		#播放反馈
	'mblog_menus_shield':True,				#屏蔽
	'mblog_menus_report':True,				#投诉
	'mblog_menus_apeal':True,				#申诉
	'mblog_menus_home':True					#返回首页
}



class MainAddon:
	def __init__(self):
		self.launch_ad_url1 = '/interface/sdk/sdkad.php'
		self.launch_ad_url2 = '/wbapplua/wbpullad.lua'

		self.card_urls = ['/cardlist', '2/page?', 'video/community_tab', '/searchall']
		self.statuses_urls = ['statuses/friends/timeline', 'statuses/unread_friends_timeline', 'statuses/unread_hot_timeline', 'groups/timeline']
		self.other_urls = {
			'/profile/me': 'remove_home',
			'/statuses/extend': 'item_extend_handler',
			'/video/remind_info': 'remove_video_remind',
			'/checkin/show': 'remove_checkin',
			'/live/media_homelist': 'remove_media_homelist',
			'/comments/build_comments': 'remove_comments',
			'/container/get_item': 'container_handler',	#列表相关
			'/profile/container_timeline': 'user_handler',		#用户主页
			'/video/tiny_stream_video_list': 'next_video_handler',		#自动下一条视频
			'/2/statuses/video_mixtimeline': 'next_video_handler',		#自动下一条视频
			'/!/client/light_skin': 'skin_handler',		#更改tab图标	 
			'/littleskin/preview': 'skin_preview_handler',
			'/search/finder': 'remove_search_main',
			'/search/container_timeline': 'remove_search',
			'/search/container_discover': 'remove_search',
			'/2/messageflow': 'remove_msg_ad',
			'/statuses/container_timeline_topic': 'topic_handler',	#超话tab
			'/push/active': 'handle_push',	# 处理一些界面设置，目前只有首页右上角红包通知
			'/statuses/container_timeline?': 'remove_main',
			'/statuses/container_timeline_unread': 'remove_main',
			# '/remind/unread_count': 'unread_count_handler',		 
		}

	# 新版主页广告地址
	def remove_main(self, data):
		items = data['items']
		new_items = []
		for item in items:
			if self.check_junk_topic(item):
				continue
			if not self.is_ad(item.get('data')):
				new_items.append(item)
		data['items'] = new_items
		print('remove_main success');


	def topic_handler(self, data):
		# print('topic_handler ing')
		items = data['items']
		new_items = []
		for c in items:
			add_flag = True
			category = c.get('category')
			if category == 'feed':
				feed_type = get_json_val(c, '$.data.buttons[0].type', True)
				if feed_type == 'follow':	# 未关注的
					add_flag = False
			elif category == 'group':
				t_content = get_json_val(c, '$.header.title.content', True)
				if t_content and '空降发帖' in t_content:
					add_flag = False
					continue
				sub_items = c.get('items')
				new_sub_items = []
				if not sub_items:
					continue
				for sub in sub_items:
					anchor_id = get_json_val(sub, '$.itemExt.anchorId', True)
					if anchor_id not in ['sg_bottom_tab_search_input', 'multi_feed_entrance', 'bottom_mix_activity', 'cats_top_content', 'chaohua_home_readpost_samecity_title', 'chaohua_discovery_banner_1', 'chaohua_home_readpost_samecity_content']:	#bottom_mix_activity-征集打卡活动 cats_top_content-超话分类 chaohua_home_readpost_samecity_title-正在讨论 banner图-banner图 chaohua_home_readpost_samecity_content-xx
						new_sub_items.append(sub)
				c['items'] = new_sub_items
			elif category == 'card':
				c_data = c.get('data', {})
				if c_data.get('top', {}).get('title') == '正在活跃':
					add_flag = False
				elif c_data.get('card_type') == 200 and c_data.get('group'):	#更多超话
					add_flag = False
			if add_flag:
				new_items.append(c)
		data['items'] = new_items
		print('remove topic success');
		# save_json_file('temp/4.json', new_items)


	def remove_search_main(self, data):
		channels = data.get('channelInfo', {}).get('channels')
		if not channels:
			return
		for channel in channels:
			payload = channel.get('payload')
			if not payload:
				continue
			self.remove_search(payload)
		print('remove_search main success');


	def check_search_window(self, item):
		if not main_config['removeSearchWindow']:
			return False
		if item.get('category') != 'card':
			return False
		item_data = item.get('data', {})
		return item_data.get('itemid') in ["finder_window", "more_frame"]


	# 发现页
	def remove_search(self, data):
		items = data.get('items')
		if not items:
			return
		new_items = []
		for item in items:
			if item.get('category') == 'feed':
				item_data = item.get('data')
				if not self.is_ad(item_data):
					new_items.append(item)
			else:
				if not self.check_search_window(item):
					new_items.append(item)
		data['items'] = new_items
		print('remove_search success');


	def remove_msg_ad(self, data):
		msgs = data.get('messages')
		if not msgs:
			return
		new_msgs = []
		for msg in msgs:
			if not msg.get('msg_card', {}).get('ad_tag'):
				new_msgs.append(msg)
		data['messages'] = new_msgs


	def remove_card_list(self, data):
		cards = data.get('cards')
		if not cards:
			return
		new_cards = []
		for c in cards:
			card_group = c.get('card_group')
			if card_group and len(card_group) > 0:
				new_group = []
				for g in card_group:
					card_type = g.get('card_type')
					if card_type not in [118, ]:
						new_group.append(g)
				c['card_group'] = new_group
				new_cards.append(c)
			else:
				if c.get('card_type') in [9, 165]:
					if not self.is_ad(c.get('mblog')):
						new_cards.append(c)
					else:
						# 广告
						pass
				else:
					new_cards.append(c)
		data['cards'] = new_cards


	# 判断首页流 感兴趣的超话
	def check_junk_topic(self, item):
		if item.get('category') != 'group':
			return False
		try:
			if item.get('items')[0]['data']['title'] == '关注你感兴趣的超话':
				return True
		except Exception as e:
			pass
		return False


	def is_ad(self, data):
		if not data:
			return False
		a = data.get('mblogtypename')
		if a and a in ['广告', '热推']:
			return True
		if data.get('promotion', {}).get('type') == 'ad':
			return True
		# if data.get('readtimetype') == 'adMblog':	#不准，很多实际非广告
		# 	return False


	def handle_comment_struct(self, data):
		if not data:
			return
		struct = data.get('common_struct')
		if not struct:
			return
		data['common_struct'] = [s for s in struct if s.get('name') != '绿洲']


	def remove_tl(self, data):
		for k in ['advertises', 'ad', 'trends']:
			if k in data:
				del data[k]
		statuses = data.get('statuses')
		if not statuses:
			return
		new_statuses = []
		for s in statuses:
			if self.is_ad(s):
				continue
			self.handle_comment_struct(s)
			new_statuses.append(s)
		data['statuses'] = new_statuses


	@except_decorative
	def remove_vip(self, item):
		header = item.get('header')
		if not header:
			return
		# vip_center = header.get('vipCenter', {})
		# if 'icon' in vip_center:
		# 	del vip_center['icon']
		# vip_center['title']['content'] = '会员中心'

		if 'vipView' in header:
			del header['vipView']


	# 将个人主页【关注】按钮默认值由【推荐】改为【关注的人】
	@except_decorative
	def update_follow_order(self, item):
		for d in item.get('items'):
			if d.get('itemId') != 'mainnums_friends':
				continue
			s = d['click']['modules'][0]['scheme']
			d['click']['modules'][0]['scheme'] = s.replace('231093_-_selfrecomm', '231093_-_selffollowed')
			print('update_follow_order success');
			return


	# 更改个人主页图标
	@except_decorative
	def update_profile_skin(self, item, k):
		profile_skin = main_config[k]
		if not profile_skin:
			return
		items = item.get('items')
		i = 0
		for d in items:
			if 'image' not in d:
				continue
			dm = d['image'].get('style', {}).get('darkMode')
			if dm != 'alpha':
				d['image']['style']['darkMode'] = 'alpha'
			d['image']['iconUrl'] = profile_skin[i]
			i += 1
			if 'dot' in d:
				del d['dot']
		print('update_profile_skin success');


	# 微博个人中心
	def remove_home(self, data):
		items = data.get('items')
		if not items:
			return
		new_items = []
		for item in items:
			item_id = item.get('itemId')
			print(item_id)
			if item_id == 'profileme_mine':
				self.remove_vip(item)
				self.update_follow_order(item)
				new_items.append(item)
			elif item_id == '100505_-_top8':
				self.update_profile_skin(item, 'profileSkin1')
				new_items.append(item)
			elif item_id == '100505_-_newcreator': #创作者中心
				if item.get('type') == 'grid':
					self.update_profile_skin(item, 'profileSkin2')
					new_items.append(item)
			elif item_id in ['mine_attent_title', '100505_-_meattent_pic', '100505_-_newusertask', '100505_-_vipkaitong', '100505_-_hongbao2022', '100505_-_adphoto', '100505_-_hongrenjie2022', '100505_-_weibonight2023']:	#为你推荐 为你推荐图片 用户任务 让红包飞 红人节 微博之夜
				continue
			elif item_id == '100505_-_advideo':
				title = get_json_val(item, '$.header.title.content', True)
				if title == '微博之夜':
					continue
			elif re.search('100505_-_meattent_-_\d+', item_id):
				continue
			else:
				new_items.append(item)
			# ['profileme_mine', '100505_-_top8', '100505_-_recentlyuser', '100505_-_chaohua', '100505_-_manage', '100505_-_manage2', '100505_-_footprint', ]:	# 个人头像 常用操作 最常访问 超话 更多功能 签到足迹
		data['items'] = new_items


	# 微博详情
	def item_extend_handler(self, data):
		save_json_file(f'temp/item-{time()}.json', data)
		if main_config['removeRelate'] or main_config['removeGood']:
			title = data.get('trend', {}).get('titles', {}).get('title')
			if main_config['removeRelate'] and title == '相关推荐':
				del data['trend']
			elif main_config['removeGood'] and title == '博主好物种草':
				del data['trend']
		if main_config['removeFollow']:
			if 'follow_data' in data:
				del data['follow_data']
		if 'reward_info' in data:
			del data['reward_info']
		if 'page_alerts' in data:
			del data['page_alerts']
		
		#广告 暂时判断逻辑根据图片	https://h5.sinaimg.cn/upload/1007/25/2018/05/03/timeline_icon_ad_delete.png
		if 'timeline_icon_ad_delete' in data.get('trend', {}).get('extra_struct', {}).get('extBtnInfo', {}).get('btn_picurl', {}):
			del data['trend']

		# 06.29 新版广告
		if 'head_cards' in data:
			del data['head_cards']

		if 'custom_action_list' in data:
			new_actions = []
			for action in data['custom_action_list']:
				_type = action.get('type')
				if _type in item_menus_config and not item_menus_config[_type]:
					pass
				else:
					print(_type)
					if _type == 'mblog_menus_copy_url':
						new_actions.insert(0, action)
					else:
						new_actions.append(action)
			data['custom_action_list'] = new_actions


	#测试 暂不知道各字段控制逻辑
	def remove_video_remind(self, data):
		data['bubble_dismiss_time'] = 0
		data['exist_remind'] = False
		data['image_dismiss_time'] = 0
		data['image'] = ''
		data['tag_image_english'] = ''
		data['tag_image_english_dark'] = ''
		data['tag_image_normal'] = ''
		data['tag_image_normal_dark'] = ''


	def remove_checkin(self, data):
		data['show'] = 0
		# data['show_time'] = 20000


	def remove_media_homelist(self, data):
		data['data'] = {}


	def remove_comments(self, data):
		del_type = ['广告',]
		if main_config['removeRelateItem']:
			del_type.append('相关内容')
		if main_config['removeRecommendItem']:
			del_type.append('推荐')
		if len(del_type) == 0:
			return
		items = data.get('datas')
		if not items:
			return
		data['datas'] = [item for item in items if item.get('adType') not in del_type]

	#超话相关
	def container_handler(self, data):
		if data.get('card_type_name') == '超话里的好友':
			print('remove 超话里的好友')
			data['card_group'] = []
		elif 'infeed_may_interest_in' in data.get('itemid', ''):
			print('remove 你可能感兴趣的超话')
			data['card_group'] = []
		elif 'infeed_friends_recommend' in data.get('itemid', ''):
			print('remove 超话好友关注')
			data['card_group'] = []


	def user_handler(self, data):
		self.remove_main(data)

		items = data['items']
		new_items = []
		for item in items:
			is_add = True
			if item.get('category') == 'group':
				try:
					if item.get('items')[0]['data']['desc'] == '可能感兴趣的人':
						is_add = False
				except Exception as e:
					pass
			if is_add:
				new_items.append(item)
		data['items'] = new_items
		print('remove_main_sub success');


	def next_video_handler(self, data):
		data['statuses'] = []
		data['tab_list'] = []


	@except_decorative
	def skin_handler(self, data):
		version = main_config.get('tabIconVersion')
		data['data']['canUse'] = 1
		if not version or version < 100:
			return
		skinList = data['data']['list']
		for skin in skinList:
			# if skin.usetime:
			# 	skin['usetime'] = 330
			skin['version'] = version
			skin['downloadlink'] = main_config['tabIconPath']
		print('tabSkinHandler success')


	def skin_preview_handler(self, data):
		data['data']['skin_info']['status'] = 1


	def unread_count_handler(self, data):
		ext = data.get('ext_new', {})
		if 'creator_task' in ext:
			ext['creator_task']['text'] = ''


	def handle_push(self, data):
		if 'floating_windows' in data:
			del data['floating_windows']

		# data['traceroute_time_interval'] = 1000
		# data['push_version'] = '1000dsadadsa'
		# data['version'] = 'version_20210128'	# 应该是这个控制版本
		# data['launch_app_config_version'] = '08e94a37bdae64de40ba6ecb16cbaa41'
		if 'feed_redpacket' in data:	# 首页右上角红包
			# data['feed_redpacket']['icon'] = 'http://h5.sinaimg.cn/upload/2016/02/04/196/helper_redpacket_valentine_compose.png'
			# data['feed_redpacket']['icon'] = 'http://p1.itc.cn/mpbp/dev/20210716/436a8ef98c8941f3ba62452b1ed4842f.jpeg'
			print(data['feed_redpacket'])


	def get_method(self, url):
		for path in self.card_urls:
			if path in url:
				return 'remove_card_list'
		for path in self.statuses_urls:
			if path in url:
				return 'remove_tl'
		for path, method in self.other_urls.items():
			if path in url:
				print(url)
				return method


	def remove_launch_ad(self, url, data):
		imgs = ["006Y6guWly1gdc0r26dwdj30ku114n4p","006Y6guWly1gdc0r1nj1oj30n01dstla","006Y6guWly1gdc0r2h1p5j30n01ds4qp","006Y6guWly1gemhviru7rj30n01dsnpe","006Y6guWly1gemhvj5se8j30n01dsag4","006Y6guWly1gdc0r3gv3sj30n01dsu0y","006Y6guWly1gdc0r3ujlxj30n01ds7qq","006Y6guWly1gdc0r4cgzwj30n01dsn3t","006Y6guWly1gdc0r4ish2j30n01dsafk"]

		if self.launch_ad_url1 in url:
			temp = re.search('\{.*\}', data)
			if not temp:
				return data
			res = json.loads(temp.group())
			if 'ads' in res:
				res['ads'] = []
				# ads = res['ads']
				# for ad in ads:
				# 	ad['imageurl'] = f'https://wx4.sinaimg.cn/mw2000/{random.choice(imgs)}.jpg'
				# 	if 'click_rects' in ad:
				# 		del ad['click_rects']
			if 'background_delay_display_time' in res:
				res['background_delay_display_time'] = 60 * 60 * 24 * 1000
			if 'show_push_splash_ad' in res:
				res['show_push_splash_ad'] = False
			return json.dumps(res) + 'OK'
		if self.launch_ad_url2 in url:
			res = json.loads(data)
			if res.get('cached_ad', {}).get('ads'):
				res['cached_ad']['ads'] = []
				return json.dumps(res)
		return data

	def test(self, flow):
		req = flow.request
		res = flow.response
		data = res.text
		# print('url', req.url)
		if '你感兴趣的超话' in data:
			print('url', req.url)
			append_txt_file(data, 'temp/4.json')
		# if('container_discover' in req.url):
		# 	append_txt_file(data, 'temp/4.json')
		# if('search/finder' in req.url):
		# 	append_txt_file(data, 'temp/5.json')


	def response(self, flow):
		req = flow.request

		# self.test(flow)

		if self.launch_ad_url1 in req.url or self.launch_ad_url2 in req.url:
			res = flow.response
			res.text = self.remove_launch_ad(req.url, res.text)
			return

		method = self.get_method(req.url)
		if not method:
			return
		res = flow.response
		data = json.loads(res.text)
		print(f'match {method}...')
		eval("self." + method)(data)
		res.text = json.dumps(data)

# mitmweb -p 8888 --listen-host 10.2.149.17
ip = '10.2.146.175'
# ip = '192.168.1.7'
port = 8888
opts = Options(listen_host=ip, listen_port=port)
opts.add_option("body_size_limit", int, 0, "")

m = DumpMaster(opts, with_termlog=False, with_dumper=False)
config = ProxyConfig(opts)
m.server = ProxyServer(config)
m.addons.add(MainAddon())

try:
	print('\nproxy:', ip, port)
	m.run()
except KeyboardInterrupt:
	m.shutdown()