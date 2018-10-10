 $(function(){ //页面ready事件
	var bgObj = chrome.extension.getBackgroundPage();
	if(bgObj){
		$('#btnStart').val(bgObj.isRunning()?'停止':'保存并开始') ;
	}
});

$('#btnStart').click(function(){//按钮点击
	var bgObj = chrome.extension.getBackgroundPage();
	if(bgObj.isRunning()){
		localStorage.RUN = "0";
		$('#btnStart').val('开始') ;
		bgObj.stop();
	}
	else{
		localStorage.RUN = "1";
		bgObj.start();	
		//关闭窗口
		window.close();
	}
	
 });
