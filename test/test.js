const version = 'v1025.2';
let $ = new nobyda();
const otherUrls = {
	// '/littleskin/lists': 'skin_list_handler',
	'/client/light_skin': 'skin_handler',		 
	// '/littleskin/preview': 'preview_handler'
}
let storeMainConfig = $.read('mainConfig');
//主要的选项配置
const mainConfig = JSON.parse(storeMainConfig);

function skin_list_handler(data) {
	skin_list_map = data['data']['type_skin_list']
	for(let [k, v] of Object.entries(skin_list_map)) {
		for (let s of v) {
			// s['download_url'] = 'https://vip.storage.weibo.com/vip_lightskin/lightskin_79_1.0.zip'
			s['mobile_thumnail'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
			s['sy_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
			s['xx_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
			s['fb_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
			s['fx_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
			s['wo_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
			s['bg_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
		}
	}
	log('skin_list_handler')
}

function preview_handler(data) {
	s = data['data']['skin_info']
	// s['skinurl'] = 'https://vip.storage.weibo.com/vip_lightskin/lightskin_79_1.0.zip'
	s['mobile_thumbnail'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
	s['sy_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
	s['xx_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
	s['fb_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
	s['fx_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
	s['wo_img'] = 'https://h5.sinaimg.cn/upload/108/914/2019/04/16/xiaowangzi_tabbar_lightskin_1.png'
	log('preview_handler')
}

function skin_handler(data) {
	let skinList = data['data']['list']
		for (let skin of skinList) {
			// if(skin.usetime) {
			// 	skin['usetime'] = 330
			// }
			log(mainConfig.tabIconPath)
			log(mainConfig.tabIconVersion)
			skin['version'] = 123
			skin['downloadlink'] = 'https://raw.fastgit.org/zmqcherish/proxy-script/main/file/skin-hebe.zip'
		}
		log('tabSkinHandler success')
}


function getModifyMethod(url) {
	for(const [path, method] of Object.entries(otherUrls)) {
		if(url.indexOf(path) > -1) {
			return method;
		}
	}
	return null;
}


function log(data) {
	console.log(data);
}


function nobyda() {
	const isQuanX = typeof $task != "undefined";
	const isSurge = typeof $httpClient != "undefined";
	const isRequest = typeof $request != "undefined";
	const notify = (title, subtitle='', message='') => {
		if (isQuanX) $notify(title, subtitle, message)
		if (isSurge) $notification.post(title, subtitle, message);
	}
	const read = (key) => {
		if (isQuanX) return $prefs.valueForKey(key);
		if (isSurge) return $persistentStore.read(key);
	}
	const done = (value = {}) => {
		if (isQuanX) return $done(value);
		if (isSurge) isRequest ? $done(value) : $done();
	}

	return {
		isRequest,
		isSurge,
		isQuanX,
		notify,
		read,
		done
	}
}

var body = $response.body;
var url = $request.url;
let method = getModifyMethod(url);
if(method) {
	log(method);
	var func = eval(method);
	let data = JSON.parse(body);
	new func(data);
	body = JSON.stringify(data);
}
$.done(body);