function clickError(){
    $('#error-dialogue').css("display","none");
    }

$(window).on('load',function(){
    $('#programspage').addClass("active");
    $(' aside .aside-container li.active').addClass('open').children('ul').show();
    $('#batch_page').addClass("active");
    ///////////////////////////////Phase session add Batches/////////
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/phasehassession/',
        type: "POST",
        dataType: "json",
        data:{"action":"view","idr":"idr"},
        success: function(response){
            var i = 0
            for (i=0;i< response.data.length;i++)
            {
                //alert(JSON.stringify(response.data[i]))
               // $('select[name="programss"] option:selected').val(response.data[i].name);
                
                    //alert(response.data[i].name)
                    var id =response.data[i]['id']
                    var name = response.data[i]['name']
                    

                 $('#add_phase').append(`<option value="${id}" selected="selected">${name}</option>`);
                    
                
            }
         

        }
    })


    //////////////////////////////////////////
    
    pagination_obj()
})
function pagination_obj(item_element)
{
    if (item_element== undefined)
    {

        $.ajax({
            url: '/api/v1/institute/batches/',
            type: "POST",
            dataType: "json",
            data:{"action":"view","page":1},
            success: function(response){
                //alert(response.data)
                if (response.status==true)
                {
                    //alert(JSON.stringify(response))
                    $('#listingtable').append('')
                    for(var i=0;i<response.data.length;i++){
                       
                        
                        $('#listingtable').append(`<tr> <td>    ${response.data[i].display_name}</td><td>${response.data[i].name}</td><td>${response.data[i].start_date}</td><td>${response.data[i].end_date}</td><td></td><td>${response.data[i].description}</td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href='javascript:void(0);' onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`)
                    
                     }
                
                     var pagi_length =response.paginations['batch_numpage']+1
                     
                     if (response.paginations['batch_numpage'] > 0){
                         if(response.paginations['batch_user_changes']==true)
                         {
                            if(response.paginations['batch_previous']==true){
    
                                $('#pagination').append(`<a href="#">prev</a>`)
                                
                            }
                            // else{
                            //     $('#pagination').append(`<span>&laquo;</span>`)
                            // }
                            for (var i=1;i<pagi_length;i++)
                            {
                             if (response.paginations['current_page']==i)
                             {
                                 
                                $('#pagination').append(`<a href="#" class="selected">${i}</a>`)
                             }  
                             else{
                                 
                                $('#pagination').append(`<a href="#" class="paginate" id="${i}" onclick="paginatin(${i});">${i}</a>`)
                             }
                            }
                            if (response.paginations['batch_next']==true)
                            {
                                $('#pagination').append(`<a href="#" onclick="paginatin(${response.paginations['class_next_page_number']});">next</a>`)
                            }
                            
                         }
                         //location.reload();
                     }
                    // alert(length(tableData))
                }
                else if (response.status == false) {
                    $("#error-msg").html(response.error[0]+" !");
                $('#error-dialogue').css("display","flex");
                }
                
            },
            error: function(response){
                $("#error-msg").html("there is problem on serverside"+" !");
                $('#error-dialogue').css("display","none");
                $('#error-dialogue').css("display","flex");
            }
        })
    }
    else{
        $.ajax({
            url: BASE_SITE_URL + '/api/v1/institute/batches/',
            type: "POST",
            dataType: "json",
            data:{"action":"view","page":item_element},
            success: function(response){
                //alert(response.data)
                if (response.status==true)
                {
                    //alert(JSON.stringify(response))
                    $('#listingtable').html('')
                    $('#pagination').html('')
                    for(var i=0;i<response.data.length;i++){
                       
                        
                        $('#listingtable').append(`<tr> <td>    ${response.data[i].display_name}</td><td>${response.data[i].name}</td><td>${response.data[i].start_date}</td><td>${response.data[i].end_date}</td><td></td><td>${response.data[i].description}</td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href='javascript:void(0);' onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`)
                    
                     }
                     //alert(JSON.stringify(response.batchee))
                     var pagi_length =response.paginations['batch_numpage']+1
                     
                     if (response.paginations['batch_numpage'] > 0){
                         
                         if(response.paginations['batch_user_changes']==true)
                         {
                            if(response.paginations['batch_previous']==true){
    
                                $('#pagination').append(`<a href="#" onclick="paginatin(${response.paginations['batch_previous_page']})">prev</a>`)
                                
                            }
                            // else{
                            //     $('#pagination').append(`<span>prev</span>`)
                            // }
                            for (var i=1;i<pagi_length;i++)
                            {
                             if (response.paginations['current_page']==i)
                             {
                                 
                                $('#pagination').append(`<a href="#" onclick="paginatin(${i}") class="selected">${i}</a>`)
                             }  
                             else{
                                 
                                $('#pagination').append(`<a href="#" class="paginate" id="${i}" onclick="paginatin(${i});">${i}</a>`)
                             }
                            }
                            if (response.paginations['batch_next']==true)
                            {
                                $('#pagination').append(`<a href="#" onclick="paginatin(${response.paginations['class_next_page_number']})">next</a>`)
                            }
                            
                         }
                         //location.reload();
                     }
                    // alert(length(tableData))
                }
                else if (response.status == false) {
                    $("#error-msg").html(response.error[0]+" !");
                $('#error-dialogue').css("display","flex");
                }
                
            },
            error: function(response){
                $("#error-msg").html("there is problem on serverside"+" !");
                $('#error-dialogue').css("display","none");
                $('#error-dialogue').css("display","flex");
            }
        })
    }
    
}
////////////////////View Id/////////////////////////////

function editClass(attrId)
{
    //dataString = {"action":"view","conditions":{"page":attrId}}
    //alert(JSON.stringify(dataString))
    var conditions = {};
        conditions.id = attrId;
        var data = {};
        data.action="view";   
        data.conditions=JSON.stringify(conditions);
        
        
    jQuery('.addSessionDialog.foredit').addClass('open');
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/batches/',
        type: "POST",
        dataType: "json",
        data:data,
        success: function(response){
            if (response.status ==true){   
                //alert(response.data)
                
                $('#title').val(response.data[0]['name'])
                //$('#startdatepicker').val(response.data[0]['start_date'])
                //$('#enddatepicker').val(response.data[0]['end_date'])
                $('#uniquecode').val(response.data[0]['display_name'])
                $('#description').val(response.data[0]['description'])
                $('#timepicker').val(response.data[0]['times_slot'])
                $('#hidden_id').val(attrId)
                var phase = response.data[0]['phase']
                

                PhaseHasSession(phase)

            }
            else{
                var class_saved = "Failed"
            }
        },
        error: function(response){
            $("#error-msg").html("there is problem on serverside"+" !");
            $('#error-dialogue').css("display","none");
            $('#error-dialogue').css("display","flex");
        }
    })
    jQuery('.addDivisionDialog.foredit').addClass('open');
    
}
function PhaseHasSession(phase)
{
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/phasehassession/',
        type: "POST",
        dataType: "json",
        data:{"action":"view","idr":"idr"},
        success: function(response){
            for (var i=0;i<=response.data.length;i++)
            {
                //alert(JSON.stringify(response.data[i]))
                if (response.data[i]['id']==phase)
                {
                   $('.progr').append(`<option value="${response.data[i]['id']}" selected="selected">${response.data[i]['name']}</option>`);
                    
                }
                else{
                    //alert(response.data[i]['id'])
                    $('.progr').append(`<option value="${response.data[i]['id']}" selected="selected">${response.data[i]['name']}</option>`);
                    
                }
            }
         

        },
        error: function(response){
            $("#error-msg").html("there is problem on serverside"+" !");
            $('#error-dialogue').css("display","none");
            $('#error-dialogue').css("display","flex");
        }
    })
}
$('#edit_batches').click( function(e){
    var name = $('#title').val()
    var start_date = $('#startdatepicker').val()
    var end_date = $('#enddatepicker').val()
   var display_name =  $('#uniquecode').val()
    var description = $('#description').val()
    var times_slot = $('#timepicker').val()
    var progr =$('.progr').val()
    var id = $('#hidden_id').val()
    //alert(progr)
    //var phase = response.data[0]['phase']
    dataString = {"action":"Update","display_name":display_name,"description":description,"name":name,"phase":progr,"start_date":start_date,"end_date":end_date,"id":id}
        
        $.ajax({
            url: BASE_SITE_URL + '/api/v1/institute/batches/',
            type: "POST",
            dataType: "json",
            data:dataString,
            success: function(response){
                if (response.status ==true){
                    var class_saved = "Success Fully Saved"
                    $('#name').val(' ')
                    $('#description').val(' ')
                    location.reload();

                }
                else if (response.status == false) {
                    $("#error-msg").html(response.error[0]+" !");
                $('#error-dialogue').css("display","flex");
                }
            },
            error: function(response){
                $("#error-msg").html("there is problem on serverside"+" !");
                $('#error-dialogue').css("display","none");
                $('#error-dialogue').css("display","flex");
            }

       })
})

//////////////////////////Add batch////////////////////

$('#add_batch').click( function(e){

    var name = $('#title_batch').val()
    var start_date = $('#startdatepicker_batch').val()
    var end_date = $('#enddatepicker_batch').val()
   var display_name =  $('#uniquecode_batch').val()
    var description = $('#description_batch').val()
    var times_slot = $('#time_batch').val()
    var phase =$('#add_phase').val()
    dataString = {"action":"add","times_slot":times_slot,"display_name":display_name,"description":description,"name":name,"phase":phase,"start_date":start_date,"end_date":end_date}
    
        
        $.ajax({
            url: BASE_SITE_URL + '/api/v1/institute/batches/',
            type: "POST",
            dataType: "json",
            data:dataString,
            success: function(response){
                if (response.status ==true){
                    var class_saved = "Success Fully Saved"
                    
                    location.reload();

                }
                else if (response.status == false) {
                $("#error-msg").html(response.error[0]+" !");
                $('#error-dialogue').css("display","flex");
                }
            },
            error: function(response){
                $("#error-msg").html("there is problem on serverside"+" !");
                $('#error-dialogue').css("display","none");
                $('#error-dialogue').css("display","flex");
            }

       })

})
function remove(removeid)
{
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/batches/',
        type: "POST",
        dataType: "json",
        data:{"action":"remove","id":removeid},
        success: function(response){
            if (response.status ==true){
                var class_saved = "Success Fully Saved"
                
                location.reload();

            }
            else{
                var class_saved = "Failed"
            }
        }

   })
}

//////////////////pagination//////

$('.paginate').click( function(e){


})

function paginatin(page_no)
{
    
    
   pagination_obj(page_no)
}
$("#add_new").click( function(e){


    //jQuery('.addSessionDialog.foredit').addClass('open');
})