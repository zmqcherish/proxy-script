
const launchAdUrls = ['/interface/sdk/sdkad.php', '/wbapplua/wbpullad.lua']

function needModify(url) {
	for (const s of launchAdUrls) {
		if(url.indexOf(s) > -1) {
			return true;
		}
	}
	return false;
}

function modifyMain(url, data) {
	for (const s of launchAdUrls) {
		if(url.indexOf(s) > -1) {
			if (data.ads) data.ads = [];
			if (data.background_delay_display_time) data.background_delay_display_time = 60 * 60 * 24 * 1000;
			if (data.show_push_splash_ad) data.show_push_splash_ad = false;
			if (data.cached_ad && data.cached_ad.ads) data.cached_ad.ads = [];
			return;
		}
	}
}

var body = $response.body;
var url = $request.url;
if(needModify(url)) {
	var obj = JSON.parse(body);
	modifyMain(url, obj);
	body = JSON.stringify(obj);
}

$done(body);