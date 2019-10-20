//唤醒文件目录展示
function FileDiv() {
	if ($("#file-div").css("display") == "none") {
		$(".files").css("display", "none");
		$("#file-div").css("display", "block");
	} else {
		$("#file-div").css("display", "none");
	}
};

//plot文件目录展示并列出文件
function FileDiv1() {
	if ($("#file-div2").css("display") == "none") {
		$(".files").css("display", "none");
		$("#plot").empty();
		$("#file-div2").css("display", "block");
		$.post(
			"/filelist/" + "plot",
			function (data) {
				console.log(data);
				for (let i = 0; i < data.length; i++) {
				const child = "<input class='plot' id='" + data[i] + "' type='checkbox' value='" + data[i] + "' " +
					"name='" + data[i] + "'><label for='" + data[i] + "'>"+ data[i] + "</label><br>";
				$("#plot").prepend(child);
				}
			});
	} else {
		$("#plot").empty();
		$("#file-div2").css("display", "none");
	}
};

// vad 文件列表
function FileVad() {
	if ($("#vad-div2").css("display") == "none") {
		$(".files").css("display", "none");
		$("#vad").empty();
		$("#vad-div2").css("display", "block");
		$.post(
			"/filelist/" + "vad",
			function (data) {
				console.log(data);
				for (let i = 0; i < data.length; i++) {
				const child = "<input class='vad' id='" + data[i] + "' type='checkbox' value='" + data[i] + "' " +
					"name='" + data[i] + "'><label for='" + data[i] + "'>"+ data[i] + "</label><br>";
				$("#vad").prepend(child);
				}
			});
	} else {
		$("#vad").empty();
		$("#vad-div2").css("display", "none");
	}
};

//隐藏目录展示并上传文件
function showFile(){
	$(".files").css("display", "table");
	$(".files").css("width", "100%");
	$("#file-div").css("display", "none");
};
function showFile2(){
	$(".files").css("display", "table");
	$(".files").css("width", "100%");
	$("#file-div2").css("display", "none");
};
function showFile3(){
	$(".files").css("display", "table");
	$(".files").css("width", "100%");
	$("#vad-div2").css("display", "none");
};

//列出文件
function FileSet(name) {
	const data_name = name.innerHTML;
	$.post(
		"/file_set/" + data_name,
		function (data) {
			// console.log(data);
			if (data_name === "pcm"){
			    $("#len").resultend(data.length);
			}
			for (let i = 0; i < data.length; i++) {
				const value_type = data_name+'*'+data[i];
				const child = "<li id='int'><input class='abc' id='" + data[i] + "' type='checkbox' className='toggle' " +
					"value='" + value_type + "' name='" + value_type + "'><label for='" + data[i] + "'>" + data[i] + "</label></li>";
				$("#" + data_name).prepend(child);
			}
		});
	if ($("#" + data_name).css("display") == "none") {
		//删除每次post请求的数重复据，所以都删除，做到刷新的作用
		$("#" + data_name).find("li").remove();
		$("#len").empty();
		$("#" + data_name).css("display", "block");
	} else {
		$("#len").empty();
		$("#" + data_name).css("display", "none");
	}
};

// 删除文件
// 1.checkbox 全选 删除全部
var file_name_arr = new Array();
const inp = document.getElementsByName("input");
function OnclikBtn() {
	for(var i = 0; i < inp.length; i++) {
		// file_name_arr.push(inp[i].name);
		if(inp[i].checked) {
			inp[i].checked = false;
			let j = file_name_arr.indexOf(inp[i].name);
			file_name_arr.splice(j, 1);
		} else {
			inp[i].checked = true;
			file_name_arr.push(inp[i].name);
		}
	}
};

// 2.checkbox 单选删除所有子文件
$('#filelist1').change(function() {//config
	const put = $("#config").find("input");
	if($(this).is(':checked')) {
		// file_name_arr.push($(this).val());
		for(let i=0;i<put.length;i++){
			if(put[i].checked) {
				put[i].checked = false;
				let j = file_name_arr.indexOf(put[i].name);
				file_name_arr.splice(j, 1);
			} else {
				put[i].checked = true;
				file_name_arr.push(put[i].name);
			}
		}
		console.log(file_name_arr)
	}
	// 父按钮点击子按钮选中，再点击子按钮取消，数据也是相同道理
	else {
		for(let i=0;i<put.length;i++){
				put[i].checked = false;
				let j = file_name_arr.indexOf(put[i].name);
				file_name_arr.splice(j, 1);
			}
	}
});

var nochick_file_name = new Array();
$('#filelist2').change(function() { //pcm
	const put = $("#pcm").find("input");
	if($(this).is(':checked')) {
		// file_name_arr.push($(this).val());
		for(let i=0;i<put.length;i++){
			if(put[i].checked) {
				put[i].checked = false;
				let j = file_name_arr.indexOf(put[i].name);
				file_name_arr.splice(j, 1);
			} else {
				put[i].checked = true;
				file_name_arr.push(put[i].name);
			}
		}
		console.log(file_name_arr)
	}
	else {
		for(let i=0;i<put.length;i++){
				put[i].checked = false;
				let j = file_name_arr.indexOf(put[i].name);
				file_name_arr.splice(j, 1);
			}
	}
});

$('#filelist3').change(function() { //result
	const put = $("#result").find("input");
	if($(this).is(':checked')) {
		// file_name_arr.push($(this).val());
		for(let i=0;i<put.length;i++){
			if(put[i].checked) {
				put[i].checked = false;
				let j = file_name_arr.indexOf(put[i].name);
				file_name_arr.splice(j, 1);
			} else {
				put[i].checked = true;
				file_name_arr.push(put[i].name);
			}
		}
		console.log(file_name_arr)
	}
	else {
		for(let i=0;i<put.length;i++){
				put[i].checked = false;
				let j = file_name_arr.indexOf(put[i].name);
				file_name_arr.splice(j, 1);
			}
	}
});

//唤醒测试点击子文件并删除
const liput = $("ol");
liput.on("change",".abc",function(){
     if($(this).is(':checked')) {
		file_name_arr.push($(this).val());
		console.log(file_name_arr)
	} else {
		let i = file_name_arr.indexOf($(this).val());
		nochick_file_name.push($(this).val());
		console.log(nochick_file_name)
		file_name_arr.splice(i, 1);
		console.log(file_name_arr)
	}
});

//plot测试点击子文件并删除
const plot_check = $("#plot");
plot_check.on("change",".plot",function(){
     if($(this).is(':checked')) {
		file_name_arr.push($(this).val());
		console.log(file_name_arr)
	} else {
		let i = file_name_arr.indexOf($(this).val());
		file_name_arr.splice(i, 1);
		console.log(file_name_arr)
	}
});

//vad测试点击子文件并删除
const vad_check = $("#vad");
vad_check.on("change",".vad",function(){
     if($(this).is(':checked')) {
		file_name_arr.push($(this).val());
		console.log(file_name_arr)
	} else {
		let i = file_name_arr.indexOf($(this).val());
		file_name_arr.splice(i, 1);
		console.log(file_name_arr)
	}
});

function DelChFile() {
	file_name_arr = file_name_arr.filter(function(n) {
		return n
	});
	$.post(
		"/DelAllFile/" + JSON.stringify(file_name_arr),
		function(data) {
			alert(data);
			window.location.reload();
		});
};

function DelVADFile() {
	file_name_arr = file_name_arr.filter(function(n) {
		return n
	});
	$.post(
		"/DelVADFile/" + JSON.stringify(file_name_arr),
		function(data) {
			alert(data);
			window.location.reload();
		});
};

function DelFile() {
	file_name_arr = file_name_arr.filter(function(n) {
		return n
	});
	if (file_name_arr.length > 100){
 	    const type = file_name_arr[0].split("*")[0]
	    if (type === "pcm"){
	    	$.post(
	                "/DelFile/" + JSON.stringify({"pcm": nochick_file_name}),
		    	function(data) {
	    	    		alert(data);
	    	    		window.location.reload();
	    		});
	    }
	    else if(type === "result"){
	    	$.post(
	        	"/DelFile/" + JSON.stringify({"result": nochick_file_name}),
			function(data) {
		    		alert(data);
		    		window.location.reload();
	    		});
	    }
	}
	else{
	    $.post(
	        "/DelFile/" + JSON.stringify({"del": file_name_arr}),
		function(data) {
		    alert(data);
		    window.location.reload();
	   });
	}
};

// function download_file() {
// 	file_name_arr = file_name_arr.filter(function(n) {
// 		return n
// 	});
// 	console.log(file_name_arr);
// 	$.post(
// 		"/download/" + JSON.stringify(file_name_arr),
// 		function(data) {
// 			alert(data)
// 		});
// };


function download_all() {
	file_name_arr = file_name_arr.filter(function(n) {
		return n
	});
	$.ajax({
		type: 'POST',
		url: /download/,
		data: JSON.stringify(file_name_arr),
		dataType: 'json',
		success: function(data) {
		},
		error: function(xhr, type) {
		}
	});
};


