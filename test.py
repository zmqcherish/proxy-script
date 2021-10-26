from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from util import *


class MainAddon:
	def __init__(self):
		self.other_urls = {
			# '/littleskin/lists': 'skin_list_handler',
			# '/client/light_skin': 'skin_handler',		#用户主页
			'/littleskin/preview': 'preview_handler',		#用户主页
			# '/littleskin/payinfo': 'payinfo_handler',		#用户主页
			# '/aj/vipcenter/home': 'vipcenter_handler',		#用户主页
		}


	def skin_list_handler(self, data):
		skin_list_map = data['data']['type_skin_list']
		for k, v in skin_list_map.items():
			for s in v:
				# s['download_url'] = 'https://vip.storage.weibo.com/vip_lightskin/lightskin_79_1.0.zip'
				s['xx_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
				s['fb_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
				s['fx_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
				s['wo_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'


	def preview_handler(self, data):
		# res_data = get_json_file('temp/2.json')
		# data['data'] = res_data['data']
		data['data']['skin_info']['status'] = 1


	
	@except_decorative
	def skin_handler(self, data):
		skin_list = data['data']['list']
		# skin_list_0 = skin_list[1]
		for skin in skin_list:
			# if skin.get('usetime'):
			# 	skin['usetime'] = 330
			skin['downloadlink'] = 'https://vip.storage.weibo.com/vip_lightskin/lightskin_79_1.0.zip'
			skin['downloadlink'] = 'https://vip.storage.weibo.com/vip_lightskin/lightskin_15_1.0.zip'
			skin['downloadlink'] = 'https://raw.fastgit.org/zmqcherish/proxy-script/main/file/skin-hebe.zip'
			# skin['skinid'] = skin_list_0['skinid']
			skin['version'] = 112


	def payinfo_handler(self, data):
		res_data = get_json_file('temp/3.json')
		# data['data'] = res_data['data']
		# data['data']['isVip'] = True
		# data['data']['vip_end_date']='2021-01-13'
		# data['data']['vip_level']= 7
		# data['data']['tipText']= '续费炫酷皮肤随心换~'
		# data['data']['tipUrl']='sinaweibo://mppopupwindow?wbx_hide_close_btn=true&wbx_bg_view_dismiss=true&scheme=sinaweibo%3A%2F%2Fwbox%3Fid%3Dn1htatg0fm%26page%3Dpages%2Fcashier%2Fcashier%26cashier_id%3D17%26F%3Dtq_skin_mppopupwindow'
		# data['data']['tipUrlNovip']='sinaweibo://mppopupwindow?wbx_hide_close_btn=true&wbx_bg_view_dismiss=true&scheme=sinaweibo%3A%2F%2Fwbox%3Fid%3Dn1htatg0fm%26page%3Dpages%2Fcashier%2Fcashier%26cashier_id%3D17%26F%3Dtq_skin_mppopupwindow'


	def vipcenter_handler(self, data):
		# res_data = get_json_file('temp/1.json')
		# data['data'] = res_data['data']
		a=1
		# user_info = data['data']['baseInfo']['user_info']
		# user_info['identity'] = '1,0'
		# user_info['level'] = 7
		# user_info['mbtype'] = 12
		# user_info['desc'] = '2022年01月13日 到期'


	def get_method(self, url):
		for path, method in self.other_urls.items():
			if path in url:
				return method



	def response(self, flow):
		req = flow.request


		method = self.get_method(req.url)
		if not method:
			return
		res = flow.response
		data = json.loads(res.text)
		print(f'match {method}...')
		eval("self." + method)(data)
		res.text = json.dumps(data)


ip = '10.2.147.8'
# ip = '192.168.1.4'
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