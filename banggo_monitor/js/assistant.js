chrome.extension.sendRequest({greeting: "isrunning"}, function(response) {
  if( response.run == "1"){
	task();
  }
  else {
  	console.info("stop");
  }
});

function GetRequest(url) {
   //var url = location.search; //获取url中"?"符后的字串
   var theRequest = new Object();
   if (url.indexOf("?") != -1) {
      var str = url.substr(1);
      strs = str.split("&");
      for(var i = 0; i < strs.length; i ++) {
         theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
      }
   }
   return theRequest;
}

function task() {
	var host = window.location.host;
	if (host == "www.banggo.com") {
		load_history_price();
	}
	if (host == "user.banggo.com") {
		if (locate_at_1th_page(window.location.search))
			add_pagination();
	}
}

function locate_at_1th_page(s) {
	if (s.indexOf("?") == -1) return true;
	var theArgs = GetRequest(s);
	if (theArgs["currentPage"] == 1) return true;
	return false;
}

function add_pagination() {
	var next_page = "<a href='/member/Collect?currentPage=2'>下一页</a>";
	var Pagination = $("div[class=mbshop_userCenterPublicPagination]");
	Pagination.append(next_page);	
}

function insert_price_text(s) {
	var mbshop_detail_baseinfo_ul = $("div[class=mbshop_detail_baseinfo] ul");
	var node_li = "<li><strong> " + s + "</strong></li";
	mbshop_detail_baseinfo_ul.append(node_li);
}

function display_history_price(l) {
	console.info(l);
	var mbshop_detail_baseinfo_ul = $("div[class=mbshop_detail_baseinfo] ul");

	var price_str = "";
	for (var i = 0; i < l.length; i ++) {
		price_str += l[i] + ", &nbsp;&nbsp;";
	}
	var node_li1 = "<li style='color: #f8584f'> <strong>历史价格为：</strong> </li";
	var node_li2 = "<li> " + price_str + "</li";
	
	mbshop_detail_baseinfo_ul.append(node_li1, node_li2);
}

function load_history_price() {
	var href = window.location.href;
	var host = window.location.host;
	var path = window.location.pathname;
	console.info(path);
	$.getJSON("http://127.0.0.1:5000/", {pathname: path}, function(data) {
		console.info(data);
		
		if (typeof(data.sku_id) == "undefined") {
			console.info("can not parse the sku id");
			insert_price_text("can not parse the sku id!");
			return;
		}
		
		if (data.price_list.length == 0) {
			insert_price_text("Not found the sku id in DataBase!");
			return;
		}
		
		display_history_price(data.price_list);
		
	});
}


