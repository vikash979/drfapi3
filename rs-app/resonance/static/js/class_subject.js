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

function editDivision(Attr,name,code,description,ms_id){
    $(`select[name="master_subject_id"] option[value="${ms_id}"]`).attr('selected', 'selected');
    $('select[name="master_subject_id"]').selectpicker('refresh');
    $('#edit_value_id').val(Attr);
    $('#label').val(name);
    $('#code').val(code);
    $('#description').val(description);
    $('#addMaterSubjectDialog').addClass('open');
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
        window.location = `/subject/class_subjects/?class=${id}`;
    }
    function failure(id){
        window.location = `/subject/class_subjects/?class=${id}`;
    }

jQuery('.add-session-link').click(function(){
    $('select[name="master_subject_id"]').selectpicker('val','');
    $('#edit_value_id').val();
    $('#label').val("");
    $('#code').val("");
    $('#description').val("");
    jQuery('#addMaterSubjectDialog').addClass('open');

});

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
    $('#successDialog').css("display","flex");
    $('#DeleteDialog').css("display","flex");


$('#classs_id, #mastersubjectdd').selectpicker(); 


// jQuery('.addDivisionDialog .form-actions a').click(function(){
//     jQuery('.addDivisionDialog').removeClass('open');
// });

// jQuery('.addDivisionDialog .form-actions a').click(function(){
//     jQuery('.addDivisionDialog.foredit').removeClass('open');
// });


});

function openTOCDialogue(subject_id,parent_id,level){
    $('#subject_id').val(subject_id);
    $('#parent_id').val(parent_id);
    $('#level').val(level);
    $('#addTOC').addClass("open");
}