from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from util import *

# proxy_data = get_json_file('proxy.json')
#微博详情页配置
item_config = {
	'removeRelate': True,	#相关推荐
	'removeGood': True,		#微博主好物种草
	'removeFollow': True,	#关注博主
}

class MainAddon:
	def __init__(self):
		self.card_urls = ['/cardlist', '/page', 'video/community_tab']
		self.statuses_urls =  ['statuses/friends/timeline', 'statuses/unread_friends_timeline', 'statuses/unread_hot_timeline', 'groups/timeline']
		self.home_url = '/profile/me'
		self.item_url = 'statuses/extend'
		# current_data = proxy_data[current_app]
		# self.target_host = current_data['host']
		# self.target_path = current_data['path']

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
		if not a:
			return False
		return a in ['广告', '热推']

	def remove_tl(self, data):
		for k in ['advertises', 'ad']:
			if k in data:
				del data[k]
		statuses = data.get('statuses')
		if not statuses:
			return
		new_statuses = []
		for s in statuses:
			if not self.is_ad(s):
				new_statuses.append(s)
		data['statuses'] = new_statuses
		# print(1111111, len(new_statuses))


	@except_decorative
	def remove_vip(self, item):
		header = item.get('header')
		if not header:
			return
		vip_center = header.get('vipCenter', {})
		del vip_center['icon']
		vip_center['title']['content'] = '会员中心'


	# 微博个人中心
	def weibo_home(self, data):
		items = data.get('items')
		if not items:
			return
		new_items = []
		for item in items:
			item_id = item.get('itemId')
			print(item_id)
			if item_id == 'profileme_mine':
				self.remove_vip(item)
			# if item_id == 'mine_attent_title':	#为你推荐
			# if item_id in ['mine_attent_title', '100505_-_meattent_pic', '100505_-_meattent_-_7469988193']:
			if item_id in ['profileme_mine', '100505_-_top8', '100505_-_recentlyuser', '100505_-_chaohua', '100505_-_manage', '100505_-_manage2']:	# 个人头像 常用操作 最常访问 超话 更多功能
				new_items.append(item)
			elif item_id == '100505_-_newcreator': #创作者中心
				if item.get('type') == 'grid':
					new_items.append(item)
		data['items'] = new_items


	# 微博详情
	def remove_item(self, data):
		if item_config['removeRelate'] or item_config['removeGood']:
			title = data.get('trend', {}).get('titles', {}).get('title')
			if item_config['removeRelate'] and title == '相关推荐':
				del data['trend']
			elif item_config['removeGood'] and title == '博主好物种草':
				del data['trend']
		if item_config['removeFollow']:
			if 'follow_data' in data:
				del data['follow_data']


	def weibo_main(self, url, data):
		for path in self.card_urls:
			if path in url:
				self.remove_card_list(data)
				return
		for path in self.statuses_urls:
			if path in url:
				self.remove_tl(data)
				return
		if self.item_url in url:
			self.remove_item(data)
			return
		if self.home_url in url:
			self.weibo_home(data)
			return
		
	def check_url(self, url):
		for path in self.card_urls:
			if path in url:
				return True
		for path in self.statuses_urls:
			if path in url:
				return True
		if self.item_url in url:
			return True
		if self.home_url in url:
			return True


	def response(self, flow):
		req = flow.request

		if 'sdkapp.uve' in req.url:
			res = flow.response
			res.text = ''
			return

		if not self.check_url(req.url):
			return
		res = flow.response
		data = json.loads(res.text)
		self.weibo_main(req.url, data)
		res.text = json.dumps(data)


ip = '10.2.146.223'
port = 8888
opts = Options(listen_host=ip, listen_port=port)
opts.add_option("body_size_limit", int, 0, "")

m = DumpMaster(opts, with_termlog=True, with_dumper=False)
config = ProxyConfig(opts)
m.server = ProxyServer(config)
m.addons.add(MainAddon())

try:
	print('\nproxy:', ip, port)
	m.run()
except KeyboardInterrupt:
	m.shutdown()