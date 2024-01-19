$(document).ready(function ()
	{

		var url1 = $("#paymentForm").attr("data-vouchers-url");
		var url2 = $("#paymentForm").attr("data-image-url");
		var nameId = $(this).val();
		$.ajax({
					url: url1,
					data: {
					  'name': nameId
					},
					success: function (data) {
					  $("#select2").html(data);
					  $("#person_image").html(data);
					}
			  });
	}.trigger('change'));