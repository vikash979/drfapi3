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

function refreshPage(){
    location.reload();
}
  
function editDivision(Attr,name,order){
    $('#edit_value_id').val(Attr);
    $('#label').val(name);
    $('#order').val(order);
    $('#addTOC').addClass("open");
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

    function success(id){
        window.location = `/subject/sub_topic/?toc=${id}`;
    }

    function failure(id){
        window.location = `/subject/sub_topic/?toc=${id}`;
    }

function filterUsingFilter(){
  var page_find = $('#pg_find').val();
  var class_filter = $( "#filter-by option:selected" ).val();
  if(class_filter!=0){
  window.location = `/subject/subjects/?page=${page_find}&class=${class_filter}`
  }
  else{
    window.location = `/subject/subjects/`  
  }
}


$(' aside .aside-container li.active').addClass('open').children('ul').show();
$('aside .aside-container li.has-sub>a').on('click', function(){
    //$(this).removeAttr('href');
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
    $('.successDialog').css("display","flex"); 


});

function openTOCDialogue(){
    $('#addTOC').addClass("open");
}