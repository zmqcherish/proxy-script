const modifyCardsUrls = ['/cardlist', '/page', 'video/community_tab'];
const modifyStatusesUrls = ['statuses/friends/timeline', 'statuses/unread_friends_timeline', 'statuses/unread_hot_timeline', 'groups/timeline'];

const otherUrls = {
	'/profile/me': 'removeHome',						//个人页模块
	'/statuses/extend': 'removeItem',					//微博详情页
	'/video/remind_info': 'removeVideoRemind',			//tab2菜单上的假通知
	'/checkin/show': 'removeCheckin',					//签到任务
	'/live/media_homelist': 'removeMediaHomelist',		//首页直播
}

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

const itemMenusConfig = {
	creator_task:false,					//转发任务
	mblog_menus_custom:false,				//寄微博
	mblog_menus_video_later:true,			//可能是稍后再看？没出现过
	mblog_menus_comment_manager:true,		//评论管理
	mblog_menus_avatar_widget:false,		//头像挂件
	mblog_menus_card_bg: false,			//卡片背景
	mblog_menus_long_picture:true,		//生成长图
	mblog_menus_delete:true,				//删除
	mblog_menus_edit:true,				//编辑
	mblog_menus_edit_history:true,		//编辑记录
	mblog_menus_edit_video:true,			//编辑视频
	mblog_menus_sticking:true,			//置顶
	mblog_menus_open_reward:true,			//赞赏
	mblog_menus_novelty:false,			//新鲜事投稿
	mblog_menus_favorite:true,			//收藏
	mblog_menus_promote:true,				//推广
	mblog_menus_modify_visible:true,		//设置分享范围
	mblog_menus_copy_url:true,			//复制链接
	mblog_menus_follow:true,				//关注
	mblog_menus_video_feedback:true,		//播放反馈
	mblog_menus_shield:true,				//屏蔽
	mblog_menus_report:true,				//投诉
	mblog_menus_apeal:true,				//申诉
	mblog_menus_home:true					//返回首页
}

const otherConfig = {
	removeLiveMedia: true,	//首页直播
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
	for(const s of Object.keys(otherUrls)) {
		if(url.indexOf(s) > -1) {
			return true;
		}
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

//移除tab2的假通知
function removeVideoRemind(data) {
	data.bubble_dismiss_time = 0;
	data.exist_remind = false;
	data.image_dismiss_time = 0;
	data.image = '';
	data.tag_image_english = '';
	data.tag_image_english_dark = '';
	data.tag_image_normal = '';
	data.tag_image_normal_dark = '';
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

	//广告 暂时判断逻辑根据图片	https://h5.sinaimg.cn/upload/1007/25/2018/05/03/timeline_icon_ad_delete.png
	try {
		let picUrl = data.trend.extra_struct.extBtnInfo.btn_picurl;
		if(picUrl.indexOf('timeline_icon_ad_delete') > -1) {
			data.trend = null;
		}
	} catch (error) {
		
	}


	if(data.custom_action_list) {
		let newActions = [];
		for (const item of data.custom_action_list) {
			let _t = action.type;
			let add = itemMenusConfig[_t]
			if(add === undefined) {
				newActions.push(item);
			} else if(_t === 'mblog_menus_copy_url') {
				newActions.unshift(item);
			} else if(add) {
				newActions.push(item);
			}
		}
		data.custom_action_list = newActions;
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
		} else if(['mine_attent_title', '100505_-_meattent_pic', '100505_-_newusertask'].indexOf(itemId) > -1) {
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


//移除tab1签到
function removeCheckin(data) {
	data.show = 0;
}


//首页直播
function removeMediaHomelist(data) {
	if(otherConfig.removeLiveMedia) {
		data.data = {};
	}
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
	for(const [path, method] of Object.entries(otherUrls)) {
		if(url.indexOf(path) > -1) {
			console.log(method);
			var func = eval(method);
			new func(data);
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