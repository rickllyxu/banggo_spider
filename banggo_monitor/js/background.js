var _staySeconds;
var _tid;
var _tabid = -1;
var _done ;

function isRunning(){
	if(localStorage.RUN == "1")
		return true;
	return false;
}
function start(){
	_done = 0;
	_staySeconds=20*1000;
	
}
function tabCreate(flag){
	var c="http://jwxk.ucas.ac.cn/courseManage/main";
	chrome.tabs.create({url:c,selected:flag},function(a){
		_tabid = a.id;
		if(localStorage.nopeople == "1" ){
			_tid=setTimeout(function(){tabDestroy()},_staySeconds);
		}
	})
}
function tabDestroy(){
	if(_tabid != -1){
		chrome.tabs.remove(_tabid);	
	}
	_tid=setTimeout(function(){tabCreate(false)},0);
}

function tabUrl(b){
	chrome.tabs.create({url:b,selected:true},function(a){})
}

function stop(){
	if(_tabid != -1){
		//chrome.tabs.remove(_tabid);	
	}
	clearTimeout(_tid);
	chrome.browserAction.setBadgeText({text:''});
	localStorage.RUN = "0";
}
chrome.extension.onRequest.addListener(
 	function(request, sender, sendResponse) {
    	if (request.greeting == "isrunning"){
      		sendResponse({run: localStorage.RUN});    		
    	}
 });
