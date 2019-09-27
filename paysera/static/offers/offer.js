window.addEventListener('load',function(){
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



        function OfferObject(formId,priceId,amountId,priceErrorId,amountErrorId,messageAreaId,messageId,messageErrorId,url){
          this.formId = $(formId);
          this.priceId = $(priceId) ;
          this.amountId = $(amountId);
          this.priceErrorId = $(priceErrorId);
          this.amountErrorId = $(amountErrorId);
          this.messageAreaId = $(messageAreaId);
          this.extraMessageId = $(messageId);
          this.extraMessageErrorId = $(messageErrorId);
          this.url = url;
        }





        var buyOffer = $("#buyOffer");
        var sellOffer = $("#sellOffer");
        var contactId = $("#contanctId");
        var notValidPrice = true;
        var notValidAmount = true;
        var notValidMessage = false;  // false, because we accept an empty message.

        var formId = $("#contactForm");
        var messageError = $("#contactMessageError");
        var messageArea = $("#contactMessageArea");
        var contactMessage = $("#contactMessage");
        var notValidContactMessage = true;

        buyOffer.click(function(){


          var offer = new OfferObject("#buyForm" ,"#buyPrice","#buyAmount" ,"#buyPriceError" ,"#buyAmountError","#messageAreaBuy","#messageBuy","#messageErrorBuy","/offers/buy/");
          offerHanlder(offer); // handle the offer click.
          handleSubmit(offer);
        });
        sellOffer.click(function(){

          var offer = new OfferObject("#sellForm","#sellPrice" , "#sellAmount", "#sellPriceError" , "#sellAmountError","#messageAreaSell","#messageSell","#messageErrorSell","/offers/sell/");
          offerHanlder(offer); // handle the offer click.
          handleSubmit(offer);
        });
        contactId.click(function(){

          contactCLick(formId,messageArea,messageError,contactMessage);
          contactSubmit(formId,messageArea,messageError,contactMessage);
        });








function offerHanlder(offer){

  window.grecaptcha.reset(0);
  window.grecaptcha.reset(1);


  offer.formId.trigger("reset");
  offer.priceErrorId.removeClass().text("");
  offer.amountErrorId.removeClass().text("");
  offer.extraMessageErrorId.removeClass().text("");
  offer.messageAreaId.removeClass().text("");

  offer.priceId.change(function(){

    offer.messageAreaId.removeClass().text("");
    notValidPrice = ( !Number(offer.priceId.val()) || Number(offer.priceId.val()) <= 0 );
    if( notValidPrice ){
      offer.priceErrorId.text("invalid price");
      offer.priceErrorId.removeClass("alert alert-success").addClass("alert alert-danger");
    }
    else{
      offer.priceErrorId.text("valid price");
      offer.priceErrorId.removeClass("alert alert-danger").addClass("alert alert-success");
    }

  });

  offer.amountId.change(function(){

    offer.messageAreaId.removeClass().text("");
    notValidAmount = ( !Number(offer.amountId.val()) || Number(offer.amountId.val()) <= 0 );
    if( notValidAmount ){
      offer.amountErrorId.text("invalid amount");
      offer.amountErrorId.removeClass("alert alert-success").addClass("alert alert-danger");
    }
    else{
      offer.amountErrorId.text("valid amount");
      offer.amountErrorId.removeClass("alert alert-danger").addClass("alert alert-success");
    }

  });

  offer.extraMessageId.change(function(){

    offer.messageAreaId.removeClass().text("");

    notValidMessage = ( offer.extraMessageId.val().length > 250 );
    if( notValidMessage ){
      offer.extraMessageErrorId.text("invalid message.").removeClass("alert alert-success").addClass("alert alert-danger");
    }
    else{
      offer.extraMessageErrorId.text("accepted.").removeClass("alert alert-danger").addClass("alert alert-success");
    }
  });


}

function handleSubmit(offer){

    offer.formId.submit(function(event){
        event.preventDefault();
        var notValidData = ( notValidPrice || notValidAmount || notValidMessage );
        if( !notValidData ){
          $.ajax({
            type : "POST",
            url : offer.url,
            data : $(this).serialize(),
            success : function(data,status,xhr){

              if(data.error){
                  var errorMsg = data.errorMsg;
                  offer.messageAreaId.text(errorMsg).removeClass("alert alert-primary").addClass("alert alert-danger");
              }
              else{
                  var message = data.message;
                  offer.formId.trigger("reset");
                  offer.priceErrorId.removeClass().text("");
                  offer.amountErrorId.removeClass().text("");
                  offer.extraMessageErrorId.removeClass().text("");
                  offer.messageAreaId.text(message).removeClass("alert alert-danger").addClass("alert alert-primary");
              }

            },
            error : function(xhr,status,data){
              console.log("Error with status : "+status);
            },

          });
          window.grecaptcha.reset(0);
          window.grecaptcha.reset(1);

        }
        else{
          var errorMsg = "invalid Data , please check it again.";
          offer.messageAreaId.text(errorMsg).removeClass("alert alert-primary").addClass("alert alert-danger");
        }



      });

  }


function contactCLick(formId , messageArea , messageError ,contactMessage){
    window.grecaptcha.reset(2);
    formId.trigger("reset");
    messageArea.removeClass().text("");
    messageError.removeClass().text("");

    contactMessage.change(function(){

      messageArea.removeClass().text("");
      notValidContactMessage = ( (contactMessage.val().length < 50) || (contactMessage.val().length > 380) || contactMessage.val().length == 0);
      if( notValidContactMessage ){
        messageError.text("invalid message.").removeClass("alert alert-success").addClass("alert alert-danger");
      }
      else{
        messageError.text("accepted.").removeClass("alert alert-danger").addClass("alert alert-success");
      }
    });
}

function contactSubmit(formId , messageArea,messageError , contactMessage){

  formId.submit(function(event){
      event.preventDefault();
      if( !notValidContactMessage ){
        $.ajax({
          type : "POST",
          url : "/notification/message/",
          data : $(this).serialize(),
          success : function(data,status,xhr){
            if(data.error){
                var errorMsg = data.errorMsg;
                messageArea.text(errorMsg).removeClass("alert alert-primary").addClass("alert alert-danger");
            }
            else{
                var message = data.message;
                formId.trigger("reset");
                messageError.removeClass().text("");
                messageArea.text(message).removeClass("alert alert-danger").addClass("alert alert-primary");
            }

          },
          error : function(xhr,status,data){
            console.log("Error with status : "+status);
          },

        });
        window.grecaptcha.reset(2);
      }
      else{
        var errorMsg = "invalid Data , please check it again.";
          messageArea.text(errorMsg).removeClass("alert alert-primary").addClass("alert alert-danger");

        }

  });


}

},true);
