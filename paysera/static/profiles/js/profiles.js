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


  var show_messages = document.getElementById("show-messages");
  var show_offers = document.getElementById("show-offers");
  var show_profile = document.getElementById("show-profile");
  var edit_profile = document.getElementById("edit-profile");
  var editProfileForm = document.getElementById("edit_profile");
  var delete_profile = document.getElementById("delete_profile");
  var messages = document.getElementById("messages");
  var offers = document.getElementById("offers");
  var profile = document.getElementById("profile");
  var alertBlock = document.getElementById("alertBlock");
  var editError = document.getElementById("editError");
  var editSuccess = document.getElementById("editSuccess");


  initialize();

  if(edit_profile){
    edit_profile.onclick = function(event){
      if(editProfileForm){
        if(editProfileForm.style.display == "none"){
          change(editProfileForm);
          var edit = $("#edit-profile-form");
          var url = edit.attr("data-url");
          console.log(url);
          if(edit){
            edit.submit(function(event){
              event.preventDefault();
              $.ajax({
                type : "POST",
                url : url,
                data : $(this).serialize(),
                success : function(data,status,xhr){
                  editError.style.display = "none";
                  location.reload(true);
                  editSuccess.style.display = "block";
                },
                error : function(xhr,status,data){
                  editSuccess.style.display = "none";
                  editError.style.display = "block";
                }
              });


            });
          }

    }
    else{
      initialize();
    }
  }
    };
  }


  if(delete_profile){

    delete_profile.onclick = function(event){

        if(alertBlock){
          if(alertBlock.style.display == "none"){
            change(alertBlock);

            var alert = document.getElementById("delete-alert");
            if(alert){
              alert.onclick = function(event){
                $.ajax({
                  type: "POST",
                  url: delete_profile.getAttribute("value"),
                  data: "no data",
                  success : function(data,status,xhr){
                    console.log("account deleted");
                    window.location.replace("/accounts/register/");
                  },
                  error : function(xhr,status,data){
                    console.log(status);
                  }
                });
              };
          }
      }
      else{
          initialize();
      }
    }
  };
  if(show_profile){
    show_profile.onclick = function(event){
      if(profile.style.display == "none"){
        change(profile);
      }
      else{
        initialize();
      }
    };

  }
  if(show_offers){

    show_offers.onclick = function(event){
      if(offers.style.display == "none"){
        change(offers);
      }
      else{
        initialize();
      }
    };
  }
  if(show_messages){
    show_messages.onclick = function(event){
      if(messages.style.display == "none"){
        change(messages);
      }
      else{
        initialize();
      }
    };
  }

}

function initialize(profileDisp="none",editProfileDisp="none",messagesDisp="none",offersDisp="none",alertBlockDisp = "none"){
      // to prevent double clicking.
    profile.style.display = profileDisp;
    messages.style.display = messagesDisp;
    offers.style.display = offersDisp;
    editProfileForm.style.display = editProfileDisp;
    alertBlock.style.display = alertBlockDisp;
    editSuccess.style.display = "none";
    editError.style.display = "none";
}
function change(item){
  initialize();
  item.style.display = "block";
}

},true);
