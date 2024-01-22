


//for enable search in drop down selection
$(document).ready(function ()
{
    $("#name").select2({});
    $("#email").select2({});
    $("#phone_no").select2({});
    $("#paginated_by").select2({});
    $("#staff").select2({});
});
//for enable search in drop down selection



 //for search menu hide and show
  $(document).ready(function(){

    var menuName = "searchMenuStateLeads"

    // Get the previous state of the menu from local storage
    var menuState = localStorage.getItem(menuName);

    // Apply the previous state to the menu
    if (menuState == "show") {
      $("#formFields").show();
        $("#showSearch").hide();
        $("#showSearch1").show();
    } else {
      $("#formFields").hide();
        $("#showSearch").show();
        $("#showSearch1").hide();
    }


      $("#showSearch").click(function()
      {
        $("#formFields").show();
        $("#showSearch").hide();
        $("#showSearch1").show();
        localStorage.setItem(menuName, "show");
      });

    $("#showSearch1").click(function()
      {
        $("#formFields").hide();
        $("#showSearch").show();
        $("#showSearch1").hide();
        localStorage.setItem(menuName, "hide");
      });
  });
  //for search menu hide and show




//for modal
document.getElementById('btn-modal').addEventListener('click', function() {
  document.getElementById('overlay').classList.add('is-visible');
  document.getElementById('modal1').classList.add('is-visible');
});
document.getElementById('close-btn').addEventListener('click', function() {
  document.getElementById('overlay').classList.remove('is-visible');
  document.getElementById('modal1').classList.remove('is-visible');
});
document.getElementById('overlay').addEventListener('click', function() {
  document.getElementById('overlay').classList.remove('is-visible');
  document.getElementById('modal1').classList.remove('is-visible');
});
//for modal

// for select tr and check checkbox
document.querySelector("table").addEventListener("click", ({target}) => {
  // discard direct clicks on input elements
  if (target.nodeName === "INPUT") return;
  // get the nearest tr
  const tr = target.closest("tr");
  if (tr) {
    // if it exists, get the first checkbox
    const checkbox = tr.querySelector("input[type='checkbox']");
    if (checkbox) {
      // if it exists, toggle the checked property
      checkbox.checked = !checkbox.checked;
    }
  }
});
// for select tr and check checkbox

// for changing color row on select
$("table").on("click", "tr", function() {
    var row = $(this);
    row.toggleClass("selected");
    row.siblings("selected").removeClass("selected");
});

// for select all checkbox
$(document).ready(function() {
    $('#select-all').click(function() {
        var checked = this.checked;
        $('input[type="checkbox"]').each(function() {
        this.checked = checked;
    });
    })
});


// For New Lead Counting
$(document).ready(function ()
	{
		var url1 = $("#lead").attr("data-count");
		var nameId = $(this).val();
		$.ajax({
					url: url1,
					data: {
					  'name': nameId
					},
					success: function (data) {
					  $("#ledCount").html(data);
					}
			  });
	});


//for lead instant update from list page
function toggle_date(link, inputField, value, Submit) {
  var link = document.getElementById(link);
  var inputField = document.getElementById(inputField);
  var submit = Submit
  var dataID = document.getElementById(value);

if (submit){
jQuery(function($) {
   var csrf_token = getCookie('csrftoken')
   var ID = Submit
   var elName = $(dataID).attr("name");
   var elValue = $(dataID).val();

   if (elName == 'f_date'){
   var date = new Date(elValue);
      day = date.getDate();
      month = date.getMonth() + 1;
      year = date.getFullYear();
      date = ([year, month, day].join('-'));
      elValue = date
   }

   var data = { "type": elName,
                "value":elValue,
                "id": ID,
                "csrfmiddlewaretoken": csrf_token

               }
    $.post("/lead_update", data);
    location.reload();
 });
 }

   if(link.style.display == 'none'){
    link.style.display = 'block';
    inputField.style.display = 'none';
    }
  else{
    link.style.display = 'none';
    inputField.style.display = 'block';
    }


    $(document).on('keyup', function(e) {
    if (e.key == "Escape") {
    link.style.display = 'block';
    inputField.style.display = 'none';
    }
    });
    $(window).click(function() {
    link.style.display = 'block';
    inputField.style.display = 'none';
    });
    $(link).click(function(event){
    event.stopPropagation();
    });
    $(inputField).click(function(event){
    event.stopPropagation();
    });

}
//for lead instant update from list page




//$('#'+submit).on("click", function () {
//   var clickedID = $(this).closest("td").attr('id');
//   var div= $('#'+clickedID);
//   var value = div.find("input");
//	$(value).each(function(){
//	  console.log(this.value);
//	});
//});



function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

