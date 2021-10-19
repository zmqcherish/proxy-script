
function nobyda() {
	const start = Date.now()
	const isRequest = typeof $request != "undefined"
	const isSurge = typeof $httpClient != "undefined"
	const isQuanX = typeof $task != "undefined"
	const isLoon = typeof $loon != "undefined"
	const isJSBox = typeof $app != "undefined" && typeof $http != "undefined"
	const isNode = typeof require == "function" && !isJSBox;
	const NodeSet = 'CookieSet.json'
	const node = (() => {
	  if (isNode) {
		const request = require('request');
		const fs = require("fs");
		const path = require("path");
		return ({
		  request,
		  fs,
		  path
		})
	  } else {
		return (null)
	  }
	})()
	const notify = (title, subtitle, message, rawopts) => {
	  const Opts = (rawopts) => { //Modified from https://github.com/chavyleung/scripts/blob/master/Env.js
		if (!rawopts) return rawopts
		if (typeof rawopts === 'string') {
		  if (isLoon) return rawopts
		  else if (isQuanX) return {
			'open-url': rawopts
		  }
		  else if (isSurge) return {
			url: rawopts
		  }
		  else return undefined
		} else if (typeof rawopts === 'object') {
		  if (isLoon) {
			let openUrl = rawopts.openUrl || rawopts.url || rawopts['open-url']
			let mediaUrl = rawopts.mediaUrl || rawopts['media-url']
			return {
			  openUrl,
			  mediaUrl
			}
		  } else if (isQuanX) {
			let openUrl = rawopts['open-url'] || rawopts.url || rawopts.openUrl
			let mediaUrl = rawopts['media-url'] || rawopts.mediaUrl
			return {
			  'open-url': openUrl,
			  'media-url': mediaUrl
			}
		  } else if (isSurge) {
			let openUrl = rawopts.url || rawopts.openUrl || rawopts['open-url']
			return {
			  url: openUrl
			}
		  }
		} else {
		  return undefined
		}
	  }
	  console.log(`${title}\n${subtitle}\n${message}`)
	  if (isQuanX) $notify(title, subtitle, message, Opts(rawopts))
	  if (isSurge) $notification.post(title, subtitle, message, Opts(rawopts))
	  if (isJSBox) $push.schedule({
		title: title,
		body: subtitle ? subtitle + "\n" + message : message
	  })
	}
	const write = (value, key) => {
	  if (isQuanX) return $prefs.setValueForKey(value, key)
	  if (isSurge) return $persistentStore.write(value, key)
	  if (isNode) {
		try {
		  if (!node.fs.existsSync(node.path.resolve(__dirname, NodeSet)))
			node.fs.writeFileSync(node.path.resolve(__dirname, NodeSet), JSON.stringify({}));
		  const dataValue = JSON.parse(node.fs.readFileSync(node.path.resolve(__dirname, NodeSet)));
		  if (value) dataValue[key] = value;
		  if (!value) delete dataValue[key];
		  return node.fs.writeFileSync(node.path.resolve(__dirname, NodeSet), JSON.stringify(dataValue));
		} catch (er) {
		  return AnError('Node.js持久化写入', null, er);
		}
	  }
	  if (isJSBox) {
		if (!value) return $file.delete(`shared://${key}.txt`);
		return $file.write({
		  data: $data({
			string: value
		  }),
		  path: `shared://${key}.txt`
		})
	  }
	}
	const read = (key) => {
	  if (isQuanX) return $prefs.valueForKey(key)
	  if (isSurge) return $persistentStore.read(key)
	  if (isNode) {
		try {
		  if (!node.fs.existsSync(node.path.resolve(__dirname, NodeSet))) return null;
		  const dataValue = JSON.parse(node.fs.readFileSync(node.path.resolve(__dirname, NodeSet)))
		  return dataValue[key]
		} catch (er) {
		  return AnError('Node.js持久化读取', null, er)
		}
	  }
	  if (isJSBox) {
		if (!$file.exists(`shared://${key}.txt`)) return null;
		return $file.read(`shared://${key}.txt`).string
	  }
	}
	const adapterStatus = (response) => {
	  if (response) {
		if (response.status) {
		  response["statusCode"] = response.status
		} else if (response.statusCode) {
		  response["status"] = response.statusCode
		}
	  }
	  return response
	}
	const get = (options, callback) => {
	  options.headers['User-Agent'] = 'JD4iPhone/167169 (iPhone; iOS 13.4.1; Scale/3.00)'
	  if (isQuanX) {
		if (typeof options == "string") options = {
		  url: options
		}
		options["method"] = "GET"
		//options["opts"] = {
		//  "hints": false
		//}
		$task.fetch(options).then(response => {
		  callback(null, adapterStatus(response), response.body)
		}, reason => callback(reason.error, null, null))
	  }
	  if (isSurge) {
		options.headers['X-Surge-Skip-Scripting'] = false
		$httpClient.get(options, (error, response, body) => {
		  callback(error, adapterStatus(response), body)
		})
	  }
	  if (isNode) {
		node.request(options, (error, response, body) => {
		  callback(error, adapterStatus(response), body)
		})
	  }
	  if (isJSBox) {
		if (typeof options == "string") options = {
		  url: options
		}
		options["header"] = options["headers"]
		options["handler"] = function(resp) {
		  let error = resp.error;
		  if (error) error = JSON.stringify(resp.error)
		  let body = resp.data;
		  if (typeof body == "object") body = JSON.stringify(resp.data);
		  callback(error, adapterStatus(resp.response), body)
		};
		$http.get(options);
	  }
	}
	const post = (options, callback) => {
	  options.headers['User-Agent'] = 'JD4iPhone/167169 (iPhone; iOS 13.4.1; Scale/3.00)'
	  if (options.body) options.headers['Content-Type'] = 'application/x-www-form-urlencoded'
	  if (isQuanX) {
		if (typeof options == "string") options = {
		  url: options
		}
		options["method"] = "POST"
		//options["opts"] = {
		//  "hints": false
		//}
		$task.fetch(options).then(response => {
		  callback(null, adapterStatus(response), response.body)
		}, reason => callback(reason.error, null, null))
	  }
	  if (isSurge) {
		options.headers['X-Surge-Skip-Scripting'] = false
		$httpClient.post(options, (error, response, body) => {
		  callback(error, adapterStatus(response), body)
		})
	  }
	  if (isNode) {
		node.request.post(options, (error, response, body) => {
		  callback(error, adapterStatus(response), body)
		})
	  }
	  if (isJSBox) {
		if (typeof options == "string") options = {
		  url: options
		}
		options["header"] = options["headers"]
		options["handler"] = function(resp) {
		  let error = resp.error;
		  if (error) error = JSON.stringify(resp.error)
		  let body = resp.data;
		  if (typeof body == "object") body = JSON.stringify(resp.data)
		  callback(error, adapterStatus(resp.response), body)
		}
		$http.post(options);
	  }
	}
	const AnError = (name, keyname, er, resp, body) => {
	  if (typeof(merge) != "undefined" && keyname) {
		if (!merge[keyname].notify) {
		  merge[keyname].notify = `${name}: 异常, 已输出日志 ‼️`
		} else {
		  merge[keyname].notify += `\n${name}: 异常, 已输出日志 ‼️ (2)`
		}
		merge[keyname].error = 1
	  }
	  return console.log(`\n‼️${name}发生错误\n‼️名称: ${er.name}\n‼️描述: ${er.message}${JSON.stringify(er).match(/\"line\"/)?`\n‼️行列: ${JSON.stringify(er)}`:``}${resp&&resp.status?`\n‼️状态: ${resp.status}`:``}${body?`\n‼️响应: ${resp&&resp.status!=503?body:`Omit.`}`:``}`)
	}
	const time = () => {
	  const end = ((Date.now() - start) / 1000).toFixed(2)
	  return console.log('\n签到用时: ' + end + ' 秒')
	}
	const done = (value = {}) => {
	  if (isQuanX) return $done(value)
	  if (isSurge) isRequest ? $done(value) : $done()
	}
	return {
	  AnError,
	  isRequest,
	  isJSBox,
	  isSurge,
	  isQuanX,
	  isLoon,
	  isNode,
	  notify,
	  write,
	  read,
	  get,
	  post,
	  time,
	  done
	}
  };