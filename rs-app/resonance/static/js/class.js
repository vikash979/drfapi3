$(window).on('load',function(){
    //$('#successDialog').css("display","flex");
    //$('#DeleteDialog').css("display","flex");
    //jQuery('.successDialog').addClass('open');

})
function clickError(){
    $('#error-dialogue').css("display","none");
    }

$(window).on('load',function(){
    $('#classsubject_page').addClass("active");
    $(' aside .aside-container li.active').addClass('open').children('ul').show();
    $('#class_page').addClass("active");
   

    
})






////////////////////////////////////////////////////////////////////////////////////////////Search//////////////////






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


