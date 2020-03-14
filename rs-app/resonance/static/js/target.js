


//////////////////////////////
/////////////////



//////////////////////////////////////remove////////////////





/////////////////////////////////////////////////////Program/////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////



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



let tableData = [
    
  
    
]


// let paginationData = [
//     { id: '1', uniquecode: 'JR', target: 'JEE MAINS and Advanced', title: 'VIJAY JR'},
//     { id: '2', uniquecode: 'G&J' , target: 'NEET', title: 'VIJAY G&J'},
//     { id: '3', uniquecode: 'JR' , target: 'Boards Revision', title: 'VIKAAS JR'},
  
// ]


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


tableData.forEach((val)=>{
    tableHTML += `<tr>
                <td><a href='program-details.html' class="title-link">${val.title}</a></td>
                <td>${val.uniquecode}</td>
                <td>${val.target}</td>
               <td class='division-actions'><a href="javascript:void(0);" class='edit-link'><i class="fa fa-pencil"></i></a><a href="#"><i class="fa fa-trash"></i></a></td>
            </tr>`;

            
});


jQuery('.listingtable').append(tableHTML);





jQuery('#txt-search').keyup(function(e){
    let searchValue = $(this).val().toLowerCase();
         console.log(searchValue);
         console.log(tableData);
         let getData = tableData.find(data => data.name === searchValue);
         console.log(getData);

    });


jQuery('.add-session-link').click(function(){
    jQuery('.addSessionDialog').addClass('open');
    jQuery('.addSessionDialog.foredit').removeClass('open');

}); 

jQuery('table td .edit-link').click(function(){
    jQuery('.addSessionDialog.foredit').addClass('open');

});  



jQuery('.addSessionDialog .form-actions a').click(function(){
    jQuery('.addSessionDialog').removeClass('open');
});



});







$('.startdatepicker').datetimepicker({
    locale: 'ru',
   debug:true,
   pickTime: false 
});

$('.enddatepicker').datetimepicker({
  locale: 'ru',
  debug:true,
  pickTime: false 

});

jQuery('.timepicker').datetimepicker({
 pickDate: false

});




// jQuery("#txt-search").change(function(){
//     alert(this.value)

// })

function program_search()
{
    // var txt-search = jQuery('#txt-search').val()
    // var session_program = jQuery('#session_program').val()
    // alert(session_program)

    var session_program = jQuery('#session_program').val()
    var  program_name = jQuery('#txt-search').val()
    var dataString = {"session_program":session_program ,"program_name":program_name}
    

    window.location.href = BASE_SITE_URL + '/institute/program_class/?session_program='+session_program+"&program_name="+program_name;
    // jQuery.ajax({
    //     url: BASE_SITE_URL + '/institute/program_class/',
    //     type: "POST",
    //     dataType: "json",
    //     data:dataString,
    //     success: function(response){
    //         console.log(JSON.stringify(response.data))
    //         if (response.status ==true){
    //            alert(response.data)

    //         }
    //         else{
    //             var class_saved = "Failed"
    //         }
           
    //     }
    // })

}