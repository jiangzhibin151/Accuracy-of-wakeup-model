//唤醒测试div
// function fwakeup() {
// 	if($("#plot-index").css("display") == "none") {
// 		if($("#wakeup-index").css("display") == "none") {
// 			$("#wakeup-index").css("display", "block")
// 		} else {
// 			$("#wakeup-index").css("display", "none")
// 		}
// 	} else {
// 		$("#plot-index").css("display", "none");
// 		$("#wakeup-index").css("display", "block")
// 	}
//
// }
//
// //画图测试div
// function fplot() {
// 	if($("#wakeup-index").css("display") == "none") {
// 		if($("#plot-index").css("display") == "none") {
// 			$("#plot-index").css("display", "block")
// 		} else {
// 			$("#plot-index").css("display", "none")
// 		}
// 	} else {
// 		$("#wakeup-index").css("display", "none");
// 		$("#plot-index").css("display", "block")
// 	}
// }
//
// var options = {
// 	bg: '#acf',
// 	// leave target blank for global nanobar
// 	target: document.getElementById('myDivId'),
// 	// id for new nanobar
// 	id: 'mynano'
// };
//
// var nanobar = new Nanobar(options);
//
// //move bar
// nanobar.go(30); // size bar 30%
//
// // Finish progress bar
// nanobar.go(100);

// 点击submit获取form表单全部数据
// $(function() {
// 	  $('#check-start').click(function() {
// 	    var d = {};
// 	    const t = $('form').serializeArray();
// 	    $.each(t, function() {
// 	      d[this.name] = this.value;
// 	    });
// 	    alert(JSON.stringify(d));
// 	  });
// });


var file_name_arr = new Array();
const inp = document.getElementsByTagName('input');

function CheckboxAll() {
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
}

// 2.checkbox 单选删除
$('input').change(function() {
	if($(this).is(':checked')) {
		file_name_arr.push($(this).val());
		console.log(file_name_arr)
	} else {
		let i = file_name_arr.indexOf($(this).val());
		file_name_arr.splice(i, 1);
		console.log(file_name_arr)
	}
});

