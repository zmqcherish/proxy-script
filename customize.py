from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from util import *


class MainAddon:
	def __init__(self):
		self.remove_vertical = True	#移除竖屏视频
		self.remove_live = True	#移除直播视频
		self.hosts = ['app.biliapi.net', 'app.bilibili.com']	#117.23.60.13
		self.url_map = {
			# 'xiaohongshu.com/api/sns/v2/system_service/splash_config': 'remove_xhs_launch',	#小红书开屏
			'x/v2/feed/index': 'remove_bb_feed'	#b站推荐页广告	app.biliapi.net
		}

	def test(self, data):
		data['cardlistInfo']['cardlist_head_cards'][0]['head_data']['midtext'] = '今日阅读1000万  今日讨论330  详情>'


	@except_decorative
	def remove_xhs_launch(self, data):
		data['data']['ads_groups'] = []


	@except_decorative
	def remove_bb_feed(self, data):
		# t = time()
		# save_json_file(f'temp/{t}.json', data)
		# if '创作推广' in json.dumps(data, ensure_ascii = False):
		# 	print(t)
		items = data['data'].get('items', [])
		if not items:
			return
		new_items = []
		for item in items:
			if item.get('ad_info'):	#包含 会员购
				continue
			goto = item.get('goto')
			if self.remove_vertical and goto == 'vertical_av':
				continue
			if self.remove_live and goto == 'live':
				continue
			banner_item = item.get('banner_item')
			if banner_item:
				item['banner_item'] = [banner for banner in banner_item if banner.get('type') != 'ad']
			new_items.append(item)
		data['data']['items'] = new_items


	def get_method(self, host, url):
		# print(url)
		# if host not in self.hosts:
		# 	return
		for path, method in self.url_map.items():
			if path in url:
				print(url)
				return method


	def response(self, flow):
		req = flow.request
		method = self.get_method(req.host, req.url)
		if not method:
			# if 'm4s' not in req.url:
			# 	f_path = f'temp/a-{time()}.txt'
			# 	append_txt_file(req.url, f_path)
			# 	d = flow.response.text
			# 	append_txt_file(d, f_path)
			return
		res = flow.response
		data = json.loads(res.text)
		print(f'match {method}...')
		eval("self." + method)(data)
		res.text = json.dumps(data)


ip = '10.2.149.17'
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
 
