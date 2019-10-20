
//进度条设置
document.getElementById('start').addEventListener('click', function() {
	// if($("#sub").css("display") == "none") {
	    $("#sub").css("display", "none");
	    $("#loding").css("display", "block")
	// }
});

//命令行设置
const nameVal = document.getElementById("info_text");
const info = document.getElementById("info")
if (nameVal == null || nameVal == "" || nameVal == undefined){
		info.style.display = 'none';
}
else {
		info.style.display = 'block';
}
