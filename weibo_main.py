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
	'profileSkin1': ["https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaingvoj6046046dg802.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaiuoxtj6046046dga02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaiytuyj60460463yv02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaj19hvj6046046aac02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaj5ka0j6046046jrp02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaj9jfmj6046046dg502.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajd0hfj60460463yu02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajfce5j6046046wet02.jpg"],
	'profileSkin2': ["https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajhmrnj6046046jro02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajmgs0j60460460t102.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajp9uuj6046046jrp02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajrwrwj6046046dg102.jpg"]
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

		self.card_urls = ['/cardlist', '/page', 'video/community_tab', '/searchall']
		self.statuses_urls = ['statuses/friends/timeline', 'statuses/unread_friends_timeline', 'statuses/unread_hot_timeline', 'groups/timeline']
		self.other_urls = {
			'/profile/me': 'remove_home',
			'/statuses/extend': 'remove_item',
			'/video/remind_info': 'remove_video_remind',
			'/checkin/show': 'remove_checkin',
			'/live/media_homelist': 'remove_media_homelist',
			'/comments/build_comments': 'remove_comments',
			'/container/get_item': 'container_handler',	#列表相关
			'/profile/statuses': 'user_handler',		#用户主页
			# '/vip_lightskin/lightskin_': 'test_func',
		}


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


	def remove_tl(self, data):
		for k in ['advertises', 'ad']:
			if k in data:
				del data[k]
		statuses = data.get('statuses')
		if not statuses:
			return
		data['statuses'] = [s for s in statuses if not self.is_ad(s)]


	@except_decorative
	def remove_vip(self, item):
		header = item.get('header')
		if not header:
			return
		vip_center = header.get('vipCenter', {})
		del vip_center['icon']
		vip_center['title']['content'] = '会员中心'


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
			# print(item_id)
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
			elif item_id in ['mine_attent_title', '100505_-_meattent_pic', '100505_-_newusertask']:	#为你推荐 为你推荐图片 用户任务
				continue
			elif re.search('100505_-_meattent_-_\d+', item_id):
				continue
			else:
				new_items.append(item)
			# ['profileme_mine', '100505_-_top8', '100505_-_recentlyuser', '100505_-_chaohua', '100505_-_manage', '100505_-_manage2', '100505_-_footprint', ]:	# 个人头像 常用操作 最常访问 超话 更多功能 签到足迹
		data['items'] = new_items


	# 微博详情
	def remove_item(self, data):
		if main_config['removeRelate'] or main_config['removeGood']:
			title = data.get('trend', {}).get('titles', {}).get('title')
			if main_config['removeRelate'] and title == '相关推荐':
				del data['trend']
			elif main_config['removeGood'] and title == '博主好物种草':
				del data['trend']
		if main_config['removeFollow']:
			if 'follow_data' in data:
				del data['follow_data']
		
		#广告 暂时判断逻辑根据图片	https://h5.sinaimg.cn/upload/1007/25/2018/05/03/timeline_icon_ad_delete.png
		if 'timeline_icon_ad_delete' in data.get('trend', {}).get('extra_struct', {}).get('extBtnInfo', {}).get('btn_picurl', {}):
			del data['trend']

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
		if not main_config['removeRelateItem']:
			return
		items = data.get('datas')
		if not items:
			return
		data['datas'] = [item for item in items if item.get('adType') != '相关内容']

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
		cards = data.get('cards')
		if not cards:
			return
		# 移除可能感兴趣的人
		data['cards'] = [c for c in cards if c.get('itemid') != 'INTEREST_PEOPLE']


	# def change_group(self, data):
	# 	gs = data.get('groups', [])
	# 	for g in gs:
	# 		if g.get('title') != '默认分组':
	# 			continue
	# 		gg = g.get('group', [])
	# 		new_group = []
	# 		for g2 in gg:
	# 			if g2.get('title') == '最新微博':
	# 				g2['type'] = 1
	# 				new_group.insert(0, g2)
	# 			else:
	# 				new_group.append(g2)
	# 		g['group'] = new_group
	# 		return

	def test_func(self, req, res):
		# if 'vip_lightskin/lightskin_' not in req.url:
		# 	return

		if 'littleskin/lists' in req.url:
			data = json.loads(res.text)
			for k,vv in data['data']['type_skin_list'].items():
				for v in vv:
					v['fx_img'] = v['fb_img']
					v['mobile_thumnail'] = v['fb_img']
			res.text = json.dumps(data)
		if 'littleskin/prev' in req.url:
			data = json.loads(res.text)
			data['data']['skin_info']['fx_img'] = data['data']['skin_info']['fb_img']
			res.text = json.dumps(data)
		pass


	def get_method(self, url):
		for path in self.card_urls:
			if path in url:
				return 'remove_card_list'
		for path in self.statuses_urls:
			if path in url:
				return 'remove_tl'
		for path, method in self.other_urls.items():
			if path in url:
				return method


	def remove_launch_ad(self, url, data):
		if self.launch_ad_url1 in url:
			temp = re.search('\{.*\}', data)
			if not temp:
				return data
			res = json.loads(temp.group())
			if 'ads' in res:
				res['ads'] = []
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


	def response(self, flow):
		req = flow.request
		# self.test_func(req, flow.response)

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


ip = '10.2.147.8'
# ip = '192.168.1.6'
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