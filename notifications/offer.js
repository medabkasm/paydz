window.onload  = function(){

  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });



        var buyOffer = $("#buyOffer");
        var sellOffer = $("#sellOffer");
        var sellNotValid
        var buyNotValid

        buyOffer.click(function(){

          $('#buyForm').trigger("reset");
          $("#buyPriceError").removeClass();
          $("#buyAmountError").removeClass();
          $("#messageAreaBuy").removeClass().text("");
          var buyPriceForm = $("#buyPrice");
          var buyAmountForm = $("#buyAmount");

          buyPriceForm.change(function(){
            var priceError = $("#buyPriceError");
            buyNotValidPrice = ( !Number(buyPriceForm.val()) || Number(buyPriceForm.val()) <= 0 );
            if( buyNotValidPrice ){
              priceError.text("invalid price");
              priceError.removeClass("alert alert-success").addClass("alert alert-danger");
            }
            else{
              priceError.text("valid price");
              priceError.removeClass("alert alert-danger").addClass("alert alert-success");
            }
          });

          buyAmountForm.change(function(){
            var amountError = $("#buyAmountError");
            buyNotValidAmount = ( !Number(buyAmountForm.val())  || Number(buyAmountForm.val()) <= 0 );
            if( buyNotValidAmount ){
              amountError.text("invalid amount");
              amountError.removeClass("alert alert-success").addClass("alert alert-danger");
            }
            else{
              amountError.text("valid amount");
              amountError.removeClass("alert alert-danger").addClass("alert alert-success");
            }

          });

        });


          var buyForm = $("#buyForm");

          buyForm.submit(function(event){

            event.preventDefault();
            var buyNotValid = ( buyNotValidPrice || buyNotValidAmount );
            if ( !buyNotValid ){
                    $.ajax({
                      method : "POST",
                      url : "/offers/buy/",
                      data : $(this).serialize(),
                      success : function(data,status,xhr){
                        if(data.error){
                            var errorMsg = data.errorMsg;
                            $("#messageAreaBuy").text(errorMsg).removeClass("alert alert-primary").addClass("alert alert-danger");
                        }
                        else{
                            var message = data.message;
                            $('#buyForm').trigger("reset");
                            $("#buyPriceError").removeClass();
                            $("#buyAmountError").removeClass();
                            $("#messageAreaBuy").text(message).removeClass("alert alert-danger").addClass("alert alert-primary");
                        }

                      },
                      error : function(xhr,status,data){
                        console.log("Error with status : "+status);
                      },
                    });
            }
            else{
              var errorMsg = "invalid Data , please check it again.";
              $("#messageAreaBuy").text(errorMsg).removeClass("alert alert-primary").addClass("alert alert-danger");
            }

            grecaptcha.reset(0);
        });



        sellOffer.click(function(){

          $('#sellForm').trigger("reset");
          $("#sellPriceError").removeClass();
          $("#sellAmountError").removeClass();
          $("#messageAreaSell").removeClass().text("");

          var sellPriceForm = $("#sellPrice");
          var sellAmountForm = $("#sellAmount");
          sellPriceForm.change(function(){

            var priceError = $("#sellPriceError");
            sellNotValidPrice = ( !Number(sellPriceForm.val()) || Number(sellPriceForm.val()) <= 0 );
            if( sellNotValidPrice ){
              priceError.text("invalid price");
              priceError.removeClass("alert alert-success").addClass("alert alert-danger");
            }
            else{
              priceError.text("valid price");
              priceError.removeClass("alert alert-danger").addClass("alert alert-success");
            }
          });
          sellAmountForm.change(function(){

            var amountError = $("#sellAmountError").removeClass();
            sellNotValidAmount = ( !Number(sellAmountForm.val()) || Number(sellAmountForm.val()) <= 0 );
            if( sellNotValidAmount ){
              amountError.text("invalid amount");
              amountError.removeClass("alert alert-success").addClass("alert alert-danger");
            }
            else{
              amountError.text("valid amount");
              amountError.removeClass("alert alert-danger").addClass("alert alert-success");
            }
          });
        });

          var sellForm = $("#sellForm");
          sellForm.submit(function(event){
            event.preventDefault();
            var sellNotValid = ( sellNotValidPrice || sellNotValidAmount );
            if(!sellNotValid){
              $.ajax({
                method : "POST",
                url : "/offers/sell/",
                data : $(this).serialize(),
                success : function(data,status,xhr){
                  if(data.error){
                      var errorMsg = data.errorMsg;

                      $("#messageAreaSell").text(errorMsg).removeClass("alert alert-primary").addClass("alert alert-danger");
                  }
                  else{
                      var message = data.message;
                      $('#sellForm').trigger("reset");
                      $("#sellPriceError").removeClass();
                      $("#sellAmountError").removeClass();
                      $("#messageAreaSell").text(message).removeClass("alert alert-danger").addClass("alert alert-primary");
                    }

                },
                error : function(xhr,status,data){
                  console.log("Error with status : "+status);
                },
              });

            }
            else{
              var errorMsg = "invalid Data , please check it again.";
              $("#messageAreaSell").text(errorMsg).removeClass("alert alert-primary").addClass("alert alert-danger");
            }
            grecaptcha.reset(1);
        });

}
