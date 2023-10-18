
$(document).ready(function(){
    $(".clickable-row").click(function(){
    //   $(this).hide();
    url__ = window.location.host + $(this).attr("custom_url")
  
    window.location.assign('http://'+url__)
    });
  });
  