//DOM Manipulation through hacky jQuery

$(".send-by li").click(function () {
    $(".send-by li").removeClass("active");
  
    $(".to-field div").addClass("hide");
    $(".btc").removeClass("hide");
    $(this).addClass("active");
  });
  
  $(".next").click(function () {
  //   $(".form-wrapper").addClass("collapse");
  
    $(".step-1").addClass("hide");
    $(".step-2").removeClass("hide");
  
    $(".step").html("Step 2 of 2");
    $(".cancel").html("Back");
  
    $(this).addClass("send");
    $(this).text("Send");
    $(this).find("i").addClass("hidden");
    setTimeout(function () {
      // $(".form-wrapper").removeClass("collapse");
    }, 1000);
  });
  
  $(".cancel").click(function () {
    // $(".form-wrapper").addClass("collapse");
  
    $(".step-2").addClass("hide");
    $(".step-1").removeClass("hide");
  
    $(".step").html("Step 1 of 2");
    $(this).html("Cancel");
  
    $(".next").removeClass("send");
    $(".next").text("Next");
    $(".next").find("i").removeClass("hidden");
    setTimeout(function () {
      $(".form-wrapper").removeClass("collapse");
    }, 1000);
  });
  
  function copyToClipboard(element) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    $(".copy-generated-address").addClass("copyed");
    setTimeout(function () {
      $(".copy-generated-address").removeClass("copyed");
    }, 5000);
    document.execCommand("copy");
    $temp.remove();
  }
  