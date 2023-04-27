//bilibili竖版视频配置
const bBConfig = {
	removeVertical: true, 	//删除竖版视频
}

function nobyda() {
	const isQuanX = typeof $task != "undefined";
	const isSurge = typeof $httpClient != "undefined";
	const isRequest = typeof $request != "undefined";
	const notify = (title, subtitle='', message='') => {
		if (isQuanX) $notify(title, subtitle, message)
		if (isSurge) $notification.post(title, subtitle, message);
	}
	const write = (value, key) => {
		if (isQuanX) return $prefs.setValueForKey(value, key);
		if (isSurge) return $persistentStore.write(value, key);
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
		write,
		read,
		done
	}
}

let $ = new nobyda();
$.write(JSON.stringify(bBConfig), 'bBConfig');
console.log($.read('bBConfig'));
console.log('success');
$.notify('bilibili配置更改成功');
$.done();
