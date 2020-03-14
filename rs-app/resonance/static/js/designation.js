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

  var pg_value = "page"+$('#pg_find').val();
  $(`#${pg_value}`).addClass('selected');

function editDivision(Attr,name){
$('#edit_value_id').val(Attr);
$('#edit_value').val(name);
$('#addDivisionDialog').addClass('open');
}

var req_id = 0;

function removeDivision(Attr){
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
    window.location = `/user/designation/`;
}
function failure(){
    window.location = `/user/designation/`;
}


jQuery('.add-division-link').click(function(){
    $('#edit_value_id').val();
    $('#edit_value').val("");
    jQuery('#addDivisionDialog').addClass('open');

});  

function clickError(){
$('#error-dialogue').css("display","none");
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
        
        $('#successDialog').css("display","flex");
        $('#DeleteDialog').css("display","flex");
       $('#namedd').selectpicker(); 

        jQuery('.addDivisionDialog .form-actions a').click(function(){
            jQuery('.addDivisionDialog').removeClass('open');
        });

         jQuery('.addDivisionDialog.foredit .form-actions a').click(function(){
            jQuery('.addDivisionDialog.foredit').removeClass('open');
        });

        

    });
