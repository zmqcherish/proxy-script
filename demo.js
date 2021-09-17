function log(msg) {
	console.log(new Date());
	console.log(msg);
}

log($request.url);
$notify('a', 'b', 'c');
var body = $response.body;
log(body);
var obj = {}
obj['success'] = true;
obj['cherish'] = 'only for hebetien';
body = JSON.stringify(obj, null, 2);
$done(body);