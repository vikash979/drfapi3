$.fn.serializeObject = function(){
    jQuery.ajaxSettings.traditional = true;
    var obj = {};
    $.each( this.serializeArray(), function(i,o){
      var n = o.name,
          v = o.value;
          obj[n] = obj[n] === undefined ? v
            : $.isArray( obj[n] ) ? obj[n].concat( v )
            : [ obj[n], v ];
    });
    return obj;
  };

  var window_url = window.location.search;
  if(window_url.length==0){
    var req_obj = [];
  }
  else{
    var req_obj=window.location.search.split("?")[1].split("&");
  }
  
  function selectFilterOption(param, val, input_val){
    c_or_not = input_val.checked;
    if(c_or_not==true){
      req_obj.push(param+"="+val);
    }
    else if(c_or_not==false){
     var index_val = req_obj.indexOf(param+"="+val);
     req_obj.splice(index_val,1);
    }
  }
  
  
  function redirecFilterPage(){
    req_param = req_obj.join("&");
    var req_url = window.location.pathname+"?"+req_param
    window.location = req_url;
  }
  
  
  for(i in req_obj){
    document.getElementById(req_obj[i]).checked = true;
  }

var pg_value = "page"+$('#pg_find').val();
$(`#${pg_value}`).addClass('selected');

function stor_update_id(Attr){
    window.location=`/user/faculties/update/${Attr}`
}

var req_id = 0;

function delete_faculty(Attr){
    req_id = Attr;
    $('.confirmationDialog').css("display","flex");
}

function confirmation(command){
    if(command=="confirm"){
        $('#delete_id').val(req_id);
        $('#remove-model').submit();
    }
    else if(command=="cancel"){
        $('.confirmationDialog').css("display","none");
    }
}

function success(){
    window.location = `/user/faculties/`;
}

function failure(){
  window.location = `/user/faculties/`;
}



        $(' aside .aside-container li.active').addClass('open').children('ul').show();
        $('aside .aside-container li.has-sub>a').on('click', function(){
            var element = $(this).parent('li');
            if (element.hasClass('open')) {
                element.removeClass('open');
                element.find('li').removeClass('open');
                element.find('ul').slideUp(200);
            }
            else {
                element.addClass('open')
                element.children('ul').slideDown(200);
                element.siblings('li').children('ul').slideUp(200);
                element.siblings('li').removeClass('open');
                element.siblings('li').find('li').removeClass('open');
                element.siblings('li').find('ul').slideUp(200);
            }
        });

         $("#upload_link").on('click', function(e){
            e.preventDefault();
            $("#upload:hidden").trigger('click');
        })

       
    

    jQuery(document).ready(function(){
        
        // $('.successDialog').css("display","flex");
        $('#failDialogue').css("display","flex");



        

    });
