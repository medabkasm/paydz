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


  //var text = $("#test").text("alert('hello')");
  var texte = document.getElementById("test");
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
  var noDataAlert = document.getElementById("no-data-alert");


  initialize();

  if(edit_profile){
    edit_profile.onclick = function(event){
      if(editProfileForm){
        if(editProfileForm.style.display == "none"){
          change(editProfileForm);
          var edit = $("#edit-profile-form");
          var url = edit.attr("data-url");
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
      var url = show_offers.getAttribute("value");
      show_data(offers,url,"offer");

    };
  }
  if(show_messages){
    show_messages.onclick = function(event){
      var url = show_messages.getAttribute("value");
      show_data(messages,url,"message");
    };
  }

}


function show_data(element,url,dataType){  // show data(messages or offers ) by setting the display attribute to block.
  if(element.style.display == "none"){
    change(element);
    get_data(element,url,dataType);
  }
  else{
    initialize();
  }
}



function get_data(dataContainer,url,dataType){   // get data(messages or offers ) form the server using ajax.

  $.ajax({
    type : "POST",
    url : url,
    data : "no data",
    success : function(data,status,xhr){
      collect_data(dataContainer,dataType,data);
    },
    error : function(xhr,status,data){
      console.error("can't get your data.");
    }


  });

}

function collect_data(dataContainer,dataType,data){ // collect ajax data , and build their box.

  dataContainer.innerHTML = '';  // empty all the child elements.

  if( data.count > 0 ){

    var data = data.dataList;
    for(var i = 0 ; i < data.length ; i ++ ){

      var col = document.createElement("div");
      var list = document.createElement("div");
      var a = document.createElement("a");
      var flex = document.createElement("div");
      var h_4 = document.createElement("h4");
      var date = document.createElement("small");
      var p = document.createElement("p");
      var type = document.createElement("small");
      var br = document.createElement("br");

      col.setAttribute("class","col-12");
      list.setAttribute("class","list-group");
      a.setAttribute("class","list-group-item list-group-item-action");
      flex.setAttribute("class","d-flex w-100 justify-content-between");
      h_4.setAttribute("class","mb-1");
      p.setAttribute("class","mb-1");
      type.setAttribute("class","type-class");

      if(dataType == "message"){
        h_4.textContent = data[i].content;
        date.textContent = data[i].date;
        p.textContent = data[i].contactMessage;
        type.textContent = dataType;
      }
      else{
        h_4.textContent = data[i].activitiy + " - " + data[i].currency;
        date.textContent = data[i].date;
        p.textContent = data[i].message;
        type.textContent = dataType;
      }



      flex.appendChild(h_4);
      flex.appendChild(date);
      a.appendChild(flex);
      a.appendChild(br);
      a.appendChild(p);
      a.appendChild(type);
      list.appendChild(a);
      col.appendChild(list);

      dataContainer.appendChild(col);
    }

  }
  else{
    change(noDataAlert);
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
    noDataAlert.style.display = "none";
}
function change(item){
  initialize();
  item.style.display = "block";
}

},true);
