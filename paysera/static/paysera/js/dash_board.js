window.addEventListener('load',function(){
  var messages = document.getElementById("messages");
  var offers = document.getElementById("offers");
  var remove_check = document.getElementsByClassName("remove-check");;

  if(messages){
    messages.addEventListener('click',function(event){
      $("#messagesBlock").toggle();
      load_remove_check(remove_check);
    });
  }
  if(offers){
    offers.addEventListener('click',function(event){
      $("#offersBlock").toggle();
      load_remove_check(remove_check);
    });
  }



function load_remove_check(obj){
if(remove_check){
  for(var i = 0 ; i < remove_check.length ; i++){
    remove_check[i].onclick = function(event){
      var obj = this;
      var text = this.textContent;
      var url = this.getAttribute("value");
      if(text == "Remove"){
            var item = this.parentElement;
            while(1){   // get the parent element of the message or the offer.
              var className = item.getAttribute("class");
              if(className == "ui items"){
                item = item.parentElement;
                break;
              }
              else{
                item = item.parentElement;
              }
            }
            $.ajax({
              type: "POST",
              url : url,
              data : "no data",
              success : function(data,status,xhr){
                item.style.display = "none";   // remove the message or the offer from display. aflter success ajax response.
              },
              error : function(xhr,status,data){
                console.log("Error with status : "+status);
              },
            });
      }
      else if (text == "Check"){

        $.ajax({
          type: "POST",
          url : url,
          data : "no data",
          success : function(data,status,xhr){
            obj.setAttribute("class","remove-check checked"); // after success ajax response.
            url = url.split("/")[0]+"/checked/"+url.split("/")[2]+"/";
            obj.setAttribute("value",url);
            obj.textContent = "Checked";
          },
          error : function(xhr,status,data){
            console.log("Error with status : "+status);
          },
        });
      }
      else{
        $.ajax({
          type: "POST",
          url : url,
          data : "no data",
          success : function(data,status,xhr){
            obj.setAttribute("class","remove-check"); // after success ajax response.
            url = url.split("/")[0]+"/check/"+url.split("/")[2]+"/";
            obj.setAttribute("value",url);
            obj.textContent = "Check";
          },
          error : function(xhr,status,data){
            console.log("Error with status : "+status);
          },
        });
      }

    };

    }

  }
  }
},true);
