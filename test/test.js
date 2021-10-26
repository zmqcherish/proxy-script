const version = 'v1026.1';
let $ = new nobyda();
const otherUrls = {
	// '/littleskin/lists': 'skin_list_handler',
	'/2/!/multimedia/playback/batch_get': 'playback_handler', 
	// '/littleskin/preview': 'preview_handler'
}
// let storeMainConfig = $.read('mainConfig');
// //主要的选项配置
// const mainConfig = JSON.parse(storeMainConfig);


function playback_handler(data) {
	let items = data.list;
	for (let item of items) {
		item.expire_time = 0;
	}
	log('playback_handler')
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