from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from util import *


class MainAddon:
	def __init__(self):
		self.url_map = {
			'xiaohongshu.com/api/sns/v2/system_service/splash_config': 'remove_xhs_launch',
		}

	@except_decorative
	def remove_xhs_launch(self, data):
		data['data']['ads_groups'] = []


	def get_method(self, url):
		for path, method in self.url_map.items():
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
 
