

//for search menu hide and show
$(document).ready(function(){
var formElement = document.getElementById("search");
var menuName = formElement.getAttribute("data-menu-name");
  
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