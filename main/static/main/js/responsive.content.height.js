//responsive table container height
$(document).ready(function () {
	var bodyHeight = window.innerHeight;
	var footerHeight = $('.footer').outerHeight(true);
	var searchHeight = $('#search').outerHeight(true);
	var formTitle = $('.form-title').outerHeight(true);
	var tittle_table_height = $("#title_table").outerHeight(true);

	if (isNaN(footerHeight)) {
		footerHeight = 0;
	}if (isNaN(searchHeight)) {
		searchHeight = 0;
	}
	if (isNaN(formTitle)) {
		formTitle = 0;
	}
	if (isNaN(tittle_table_height)) {
		tittle_table_height = 0;
	}

	$("#main_container").css("height", bodyHeight - 55 - footerHeight);
	var mainHeight = $("#main_container").outerHeight(true);

	var contentHeight = mainHeight - searchHeight - formTitle - tittle_table_height - 10;
//	console.log('form title :', $('.form-title'));
//	console.log('form title Height:', formTitle);
//	 console.log('Search Height:', searchHeight);
//	 console.log('Content:', contentHeight);
//	 console.log('Main Height:', mainHeight);
	$('.table-container').css('height', contentHeight);
});
