
const modifyCardsUrls = ['/cardlist', '/page', 'video/community_tab'];
const modifyStatusesUrls = ['statuses/friends/timeline', 'statuses/unread_friends_timeline', 'statuses/unread_hot_timeline', 'groups/timeline'];
const homeUrl = '/profile/me';
const itemUrl = 'statuses/extend'

//个人中心移除选项配置，多数是可以直接在微博的更多功能里直接移除
const homeConfig = {
	removeVip: true,			//移除头像旁边的vip样式
	removeCreatorTask: true,	//移除创作者中心下方的轮播图
}

//微博详情页配置
const itemConfig = {
	removeRelate: true,		//相关推荐
	removeGood: true,		//微博主好物种草
	removeFollow: true,		//关注博主
}

let isDebug = false;

function needModify(url) {
	for (const s of modifyCardsUrls) {
		if(url.indexOf(s) > -1) {
			return true;
		}
	}
	for (const s of modifyStatusesUrls) {
		if(url.indexOf(s) > -1) {
			return true;
		}
	}
	if(url.indexOf(homeUrl) > -1 || url.indexOf(itemUrl) > -1) {
		return true;
	}
	return false;
}


function isAd(data) {
	if(!data) {
		return false;
	}
	return data.mblogtypename == '广告' || data.mblogtypename == '热推';
}

function removeCards(data) {
	if(!data.cards) {
		return;
	}
	let newCards = [];
	for (const card of data.cards) {
		let cardGroup = card.card_group;
		if(cardGroup && cardGroup.length > 0) {
			let newGroup = [];
			for (const group of cardGroup) {
				let cardType = group.card_type;
				if(cardType != 118) {
					newGroup.push(group);
				}
			}
			card.card_group = newGroup;
			newCards.push(card);
		} else {
			let cardType = card.card_type;
			if([9,165].indexOf(cardType) > -1) {
				if(!isAd(card.mblog)) {
					newCards.push(card);
				}
			} else {
				newCards.push(card);
			}
		}
	}
	data.cards = newCards;
}


function removeTimeLine(data) {
	if(data.ad) {
		data.ad = [];
	}
	if(data.advertises) {
		data.advertises = [];
	}
	if(!data.statuses) {
		return;
	}
	let newStatuses = [];
	for (const s of data.statuses) {
		if(!isAd(s)) {
			newStatuses.push(s);
		}
	}
	data.statuses = newStatuses;
}


function removeVip(data) {
	if(!data.header) {
		return data;
	}
	let vipCenter = data.header.vipCenter;
	if(!vipCenter) {
		return data;
	}
	vipCenter.icon = '';
	vipCenter.title.content = '会员中心';
	return data;
}


//微博详情页
function removeItem(data) {
	if(itemConfig.removeRelate || itemConfig.removeGood) {
		if(data.trend && data.trend.titles) {
			let title = data.trend.titles.title;
			if(itemConfig.removeRelate && title === '相关推荐') {
				data.trend = null;
			} else if (itemConfig.removeGood && title === '博主好物种草') {
				data.trend = null;
			}
		}
	}
	if(itemConfig.removeFollow) {
		if(data.follow_data) {
			data.follow_data = null;
		}
	}
}

function removeHome(data) {
	if(!data.items) {
		return data;
	}
	let newItems = [];
	for (let item of data.items) {
		let itemId = item.itemId;
		if(itemId == 'profileme_mine') {
			if(homeConfig.removeVip) {
				item = removeVip(item);;
			}
			newItems.push(item);
		} else if (itemId == '100505_-_newcreator') {
			if(homeConfig.removeCreatorTask) {
				if(item.type == 'grid') {
					newItems.push(item);
				}
			} else {
				newItems.push(item);
			}
		} else if(['mine_attent_title', '100505_-_meattent_pic'].indexOf(itemId) > -1) {
			continue;
		} else if (itemId.match(/100505_-_meattent_-_\d+/)) {
			continue;
		} else {
			newItems.push(item);
		}
	}
	data.items = newItems;
	return data;
}


function modifyMain(url, data) {
	if(isDebug) {
		console.log(new Date());
		console.log(url);
	}
	for (const s of modifyCardsUrls) {
		if(url.indexOf(s) > -1) {
			removeCards(data);
			return;
		}
	}
	for (const s of modifyStatusesUrls) {
		if(url.indexOf(s) > -1) {
			removeTimeLine(data);
			return;
		}
	}
	if(url.indexOf(homeUrl) > -1) {
		removeHome(data);
		return;
	}
	if(url.indexOf(itemUrl) > -1) {
		removeItem(data);
		return;
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