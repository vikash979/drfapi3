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

    $(window).on('load',function(){
        $.ajax({
                url:`/institute/csc_finder?type=1`,
                type: "GET",
                dataType: "json",
                success: function(response){
                    if (response.status != false) {
                        $('#countrydd').empty();
                        $('#countrydd').append(`<option value="" selected disabled>Select Country</option>`);
                        for(var i=0;i<response.data.length;i++){
                            $('#countrydd').append(`<option value="${response.data[i].id}">${response.data[i].label}</option>`);
                        }
                        $('#countrydd').selectpicker('refresh');
                }
            }
               
            });
        });

function SelectState(){
    var selected_country =$( "#countrydd option:selected" ).val();
    $.ajax({
        url:`/institute/csc_finder?type=2&parent=${selected_country}`,
        type: "GET",
        dataType: "json",
        success: function(response){
            if (response.status != false) {
                $('#statedd').empty();
                $('#statedd').append(`<option value="" selected disabled>Select State</option>`);
                $('#citydd').empty();
                $('#citydd').append(`<option value="" selected disabled>Select City</option>`);
                for(var i=0;i<response.data.length;i++){
                    $('#statedd').append(`<option value="${response.data[i].id}">${response.data[i].label}</option>`);
                    
                }
                $('#statedd').selectpicker('refresh');
        }
    }
       
    });
}

function SelectCity(){
    var selected_state =$( "#statedd option:selected" ).val();
    $.ajax({
        url:`/institute/csc_finder?type=3&parent=${selected_state}`,
        type: "GET",
        dataType: "json",
        success: function(response){
            if (response.status != false) {
                $('#citydd').empty();
                $('#citydd').append(`<option value="" selected disabled>Select City</option>`);
                for(var i=0;i<response.data.length;i++){
                    $('#citydd').append(`<option value="${response.data[i].id}">${response.data[i].label}</option>`);
                    
                }
                $('#citydd').selectpicker('refresh');
        }
    }
       
    });
}

var pg_value = "page"+$('#pg_find').val();
$(`#${pg_value}`).addClass('selected');

function refreshPage(){
    location.reload();
}

function editDivision(Attr,name,country,state,city){
    $('#edit_value_id').val(Attr);
    $('#name').val(name);
    $(`select[name="country_id"] option[value="${country}"]`).attr('selected', 'selected');
    $('#countrydd').selectpicker('refresh');
    jQuery('.addCentersDialog').addClass('open');
    $.ajax({
        url:`/institute/csc_finder?type=2&parent=${country}`,
        type: "GET",
        dataType: "json",
        success: function(response){
            if (response.status != false) {
                $('#statedd').empty();
                $('#statedd').append(`<option value="" selected disabled>Select State</option>`);
                $('#citydd').empty();
                $('#citydd').append(`<option value="" selected disabled>Select City</option>`);
                for(var i=0;i<response.data.length;i++){
                    $('#statedd').append(`<option value="${response.data[i].id}">${response.data[i].label}</option>`);
                    
                }
                $(`select[name="state_id"] option[value="${state}"]`).attr('selected', 'selected');
                $('#statedd').selectpicker('refresh');
        }
    }
       
    });

    $.ajax({
        url:`/institute/csc_finder?type=3&parent=${state}`,
        type: "GET",
        dataType: "json",
        success: function(response){
            if (response.status != false) {
                $('#citydd').empty();
                $('#citydd').append(`<option selected disabled>Select City</option>`);
                for(var i=0;i<response.data.length;i++){
                    $('#citydd').append(`<option value="${response.data[i].id}">${response.data[i].label}</option>`);
                }
                $('#citydd').selectpicker('refresh');
                $(`select[id="citydd"] option[value="${city}"]`).attr('selected', 'selected');
                $('#citydd').selectpicker('refresh');
        }
    }
       
    });

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
        window.location = `/institute/centers/`;
    }
    function failure(){
        window.location = `/institute/centers/`;
    }

jQuery('.add-center-link').click(function(){
    // $('select[id="countrydd"]').selectpicker('val','');
    // $('select[id="statedd"]').selectpicker('val','');
    // $('select[id="citydd"]').selectpicker('val','');
    // $('#name').val("");
    jQuery('.addCentersDialog').addClass('open');

});


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


$('#countrydd, #regiondd, #statedd, #citydd').selectpicker(); 


jQuery('.addDivisionDialog .form-actions a').click(function(){
    jQuery('.addDivisionDialog').removeClass('open');
});

jQuery('.addDivisionDialog .form-actions a').click(function(){
    jQuery('.addDivisionDialog.foredit').removeClass('open');
});


});
