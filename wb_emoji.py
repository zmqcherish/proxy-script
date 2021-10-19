from util import *
from bs4 import BeautifulSoup

#需要在config文件中配置cookie信息
config = get_json_file('file/config_private.json') or get_json_file('file/config.json')
cookie = config.get('cookie')

headers = {
	'Host': 'new.vip.weibo.cn',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Cookie': cookie,
	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Weibo (iPhone12,1__weibo__11.10.0__iphone__os15.0.2)'
}

def download_pkg(pid):
	path = f'imgs/weibo/{pid}'
	create_folder(path)
	res = requests.get(f'https://new.vip.weibo.cn/gifimg/detail?ua=iPhone12%2C1__weibo__11.10.0__iphone__os15.0.2&from=10BA093010&pkg_id={pid}', headers=headers)

	soup = BeautifulSoup(res.text)
	cover = soup.img
	urlretrieve(cover['src'], f'{path}/cover.png')
	imgs = soup.find(id='emojibox').find_all('div', {'node-type':True})
	i = 1
	for img in imgs:
		src = img['data-src']
		append_txt_file(src, f'{path}/imgs.txt')
		urlretrieve(src, f'{path}/{i}{get_file_suffix(src)}')
		# urlretrieve(src, f'{path}/{i}.gif')
		i += 1
pk_list = [116, 156, 159]
for pid in pk_list:
	download_pkg(pid)

