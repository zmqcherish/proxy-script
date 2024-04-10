from util import *

class MainAddon:
	def __init__(self):
		self.other_urls = {
			# '/2/!/multimedia/playback/batch_get': 'playback_handler',		#用户主页
			# '/remind/unread_count': 'unread_count_handler',		#用户主页
			'/batch': 'wyy',		#用户主页
			'/api/v3/song/detail': 'wyy',		#用户主页
			'/api/v6/playlist/detail': 'wyy',		#用户主页
			'/api/song/enhance/player/url': 'wyy',		#用户主页
		}


	def unread_count_handler(self, data):
		pass


	def playback_handler(self, data):
		if 'list' not in data:
			return
		save_pickle('temp/playback', data)
		llist = data['list']
		for item in llist:
			if 'ui' in item:
				item['ui']['cast_scheme'] = ''
			item['expire_time'] = 0
			item['media_id'] = 0
			if 'details' in item:
				details = item['details']
				for detail in details:
					if 'play_info' in detail:
						del detail['play_info']
					if 'meta' in detail:
						del detail['meta']
		print(data)


	
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


	def wyy(self, data):
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
		res = flow.response

		
		# if '京东' in res_text:
		# 	print('aaaa', req.url)

		method = self.get_method(req.url)
		if not method:
			return
		res_text = res.text
		data = json.loads(res.text)
		print(f'match {method}...')
		eval("self." + method)(data)
		res.text = json.dumps(data)
