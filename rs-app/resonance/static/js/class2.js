$(window).on('load',function(){
    $('#classsubject_page').addClass("active");
    $(' aside .aside-container li.active').addClass('open').children('ul').show();
    $('#class_page').addClass("active");
    


//////////////////////////////Views class/////////////////////////////////

    classpagination()
})

$("#addclass").click( function(e){
    $('.heading').text('Add Class')
    
    var display_name = $('#title').val()
    var description = $('#description').val()
    var name = $('#shortcode').val()
    var order = $('#order').val()
   // alert(JSON.stringify({"action":"add","display_name":display_name,"description":description,"name":name,"order":order}))
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/institutes/',
        type: "POST",
        dataType: "json",
        data:{"action":"add","display_name":display_name,"description":description,"name":name,"order":order},
        success: function(response){
            console.log(JSON.stringify(response.data))
            if (response.status ==true){
                var class_saved = "Success Fully Saved"
                $('#title').val(' ')
                $('#description').val(' ')
                location.reload();

            }
            else{
                var class_saved = "Failed"
            }
           
        }
    })
    
})

function classpagination(class_count)
{
    if (class_count== undefined)
    {
        $.ajax({
            url: BASE_SITE_URL + '/api/v1/institute/institutes/',
            type: "POST",
            dataType: "json",
            data:{"action":"view"},
            success: function(response){
                if (response.status==true)
                {
                    let lineNo = 1;
                    tableBody = $("table tbody");
                    let tableData = JSON.stringify(response.data)
                    $('#listingtable').html('')
                    $('#pagination').html('')
                    for(var i=0;i<response.data.length;i++){
                 
                    var totalrecord = (response.data[i].id+"_"+response.data[i].display_name+"_"+response.data[i].order+"_"+response.data[i].name+"_"+response.data[i].description)
                   
                    $('#listingtable').append(`<tr> <td>    ${response.data[i].display_name}</td><td>${response.data[i].order}</td><td>${response.data[i].name}</td><td>${response.data[i].description}</td><td><a href="class-subjects-details.html" class=' create-subjects-link'><i class="fa fa-plus"></i>Create  Subjects</a></td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href="#" onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`)
                   
                    }
                    var pagi_length =response.paginations['class_numpage']+1
                     
                    if (response.paginations['class_numpage'] > 0){
                        if(response.paginations['class_user_changes']==true)
                        {
                           if(response.paginations['class_previous']==true){
   
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
                                
                               $('#pagination').append(`<a href="#" class="paginate" id="${i}" onclick="classpagination(${i});">${i}</a>`)
                            }
                           }
                           if (response.paginations['class_next']==true)
                           {
                               $('#pagination').append(`<a href="#" onclick="classpagination(${response.paginations['class_next_page_number']});">next</a>`)
                           }
                           
                        }
                        //location.reload();
                    }
                }
                
            }
        })
    }
    else{

        $.ajax({
            url: BASE_SITE_URL + '/api/v1/institute/institutes/',
            type: "POST",
            dataType: "json",
            data:{"action":"view","page":class_count},
            success: function(response){
                if (response.status==true)
                {
                    $('#listingtable').html('')
                     $('#pagination').html(' ')
                    for(var i=0;i<response.data.length;i++){
                    
                    var totalrecord = (response.data[i].id+"_"+response.data[i].display_name+"_"+response.data[i].order+"_"+response.data[i].name+"_"+response.data[i].description)
                    //alert(totalrecord)
                    $('#listingtable').append(`<tr> <td>    ${response.data[i].display_name}</td><td>${response.data[i].order}</td><td>${response.data[i].name}</td><td>${response.data[i].description}</td><td><a href="class-subjects-details.html" class=' create-subjects-link'><i class="fa fa-plus"></i>Create  Subjects</a></td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href="#" onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`)
                  
                    }
                    var pagi_length =response.paginations['class_numpage']+1
                     
                    if (response.paginations['class_numpage'] > 0){
                        
                        if(response.paginations['class_user_changes']==true)
                        {
                           if(response.paginations['class_previous']==true){
   
                               $('#pagination').append(`<a href="#" onclick="classpagination(${response.paginations['class_previous_page']})">prev</a>`)
                               
                           }
                           // else{
                           //     $('#pagination').append(`<span>prev</span>`)
                           // }
                           for (var i=1;i<pagi_length;i++)
                           {
                            if (response.paginations['current_page']==i)
                            {
                                
                               $('#pagination').append(`<a href="#" onclick="classpagination(${i}") class="selected">${i}</a>`)
                            }  
                            else{
                                
                               $('#pagination').append(`<a href="#" class="paginate" id="${i}" onclick="classpagination(${i});">${i}</a>`)
                            }
                           }
                           if (response.paginations['class_next']==true)
                           {
                               $('#pagination').append(`<a href="#" onclick="classpagination(${response.paginations['class_next_page_number']})">next</a>`)
                           }
                           
                        }
                        //location.reload();
                    }
                }
                
            }
        })
    }
  

}
function remove(removeid)
{
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/institutes/',
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




////////////////////////////////////////////////////////////////////////////////////////////Search//////////////////


function class_filter(value)
{
    var conditions = {};
        conditions.name = value;
        var data = {};
        data.action="view";   
        data.conditions=JSON.stringify(conditions);
        //alert(JSON.stringify(data))
        $.ajax({
            url: BASE_SITE_URL + '/api/v1/institute/institutes/',
            type: "POST",
            dataType: "json",
            data:data,
            success: function(response){
               
                //alert(JSON.stringify(response.data))
                $('#listingtable').html('')
                for(var i=0;i<response.data.length;i++){
                   // alert(JSON.stringify(response.data))
                    
                   // var totalrecord = (response.data[i].id+"_"+response.data[i].display_name+"_"+response.data[i].order+"_"+response.data[i].name+"_"+response.data[i].description)
                    //alert(totalrecord)
                  $('#listingtable').append(`<tr> <td>    ${response.data[i].display_name}</td><td>${response.data[i].order}</td><td>${response.data[i].name}</td><td>${response.data[i].description}</td><td><a href="class-subjects-details.html" class=' create-subjects-link'><i class="fa fa-plus"></i>Create  Subjects</a></td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href="#" onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`)
                  
                    }
                // var display_name = $('#title').val(' ')
                // var description = $('#description').val(' ')
                // var name = $('#shortcode').val(' ')
                // var order = $('#order').val(' ')
                // location.reload();
    
            }
        })
       
}





///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// $(' aside .aside-container li.active').addClass('open').children('ul').show();
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

let tableData = [
    { id: '1', subject: 'Physics,Math,Chemistry', sequencenumber: '1', shortcode: 'XI', title: 'XI',description: 'Eleven'},
    { id: '2', subject: 'Physics,Math,Chemistry',sequencenumber: '2', shortcode: 'XII' , title: 'XII' ,description: 'Tweleve'},
    { id: '3', subject: 'Physics,Math,Chemistry', sequencenumber: '3', shortcode: 'XIII' , title: 'Droppers' ,description: 'Droppers'},
    
  
    
]


let paginationData = [
    { id: '1', subject: 'Subjectname1', sequencenumber: '4', shortcode: '123434', title: 'title1',description: 'description1'},
    { id: '2', subject: 'Subjectname2',sequencenumber: '5', shortcode: 'ycyyde' , title: 'title2' ,description: 'description2'},
    { id: '3', subject: 'Subjectname3', sequencenumber: '3', shortcode: '5hhfyr' , title: 'title3' ,description: 'description3'},
    { id: '4', subject: 'Subjectname4', sequencenumber: '2', shortcode: '9lgiyy' , title: 'title4' ,description: 'description4'},
    { id: '5', subject: 'Subjectname5', sequencenumber: '1', shortcode: '857ffg' , title: 'title5' ,description: 'description5'},
    { id: '6', subject: 'Subjectname6', sequencenumber: '6', shortcode: '855jfuy' , title: 'title6' ,description: 'description6'},
]


     function confirmation(type){
         if (type === 'confirm'){
            console.log("confirm");
         }else{
           console.log("cancel"); 
         }  
    }

    function success(type){
         if (type === 'ok'){
            console.log("ok");
         }else{
           console.log("cancel"); 
         }  
    }


jQuery(document).ready(function(){




let tableHTML ='';
let paginationHTML ='';




jQuery('.listingtable').append(tableHTML);





jQuery('#txt-search').keyup(function(e){
    let searchValue = $(this).val().toLowerCase();
         console.log(searchValue);
         console.log(tableData);
         let getData = tableData.find(data => data.name === searchValue);
         console.log(getData);

    });


jQuery('.add-session-link').click(function(){
    //jQuery('.filter-section').css('display','flex');
    //jQuery('.datepicker').datetimepicker();  
    jQuery('.addSessionDialog').addClass('open');
    jQuery('.addSessionDialog.foredit').removeClass('open');

}); 

jQuery('table td .edit-link').click(function(){
    jQuery('#addSessionDialog').addClass('open');

});  



jQuery('.addSessionDialog .form-actions a').click(function(){
    jQuery('.addSessionDialog').removeClass('open');
});

 jQuery('.addSessionDialog.foredit .form-actions a').click(function(){
    jQuery('.addSessionDialog.foredit').removeClass('open');
});



});


