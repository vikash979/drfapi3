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

  function clickError(){
    $('#error-dialogue').css("display","none");
    }
    
var page_count = 1;
var max_page = 0;

$(window).on('load',function(){
    $('#classsubject_page').addClass("active");
    $(' aside .aside-container li.active').addClass('open').children('ul').show();
    $('#concept_page').addClass("active");
    var department_count = 0;
    var conditions = {};
    var paginations = {};
    paginations.page = 1;
    var data = {};
    data.action="view";   
    data.conditions=JSON.stringify(conditions);
    data.paginations = JSON.stringify(paginations);
    $.ajax({
            url: BASE_SITE_URL + `/api/v1/auth/skill/`,
            type: "POST",
            dataType: "json",
            data:data,
            success: function(response){
                if (response.status != false) {
                    for(var i=0;i<response.data.length;i++){
                        $('.listingtable').append(`<tr>
                                        <td>${response.data[i].skill}</td>
                                       <td>subject1</td>
                                       <td><a href="javascript:void(0);" class='edit-link' onclick="editDivision(${response.data[i].id})"><i class="fa fa-pencil"></i></a><a href="javascript:void(0);" onclick="removeDivision(${response.data[i].id})"><i class="fa fa-trash"></i></a></td>
                                    </tr>`);
                        department_count+=1;
                    }
                    $('#division_count').html(department_count);
                    var prev = `<a href="javascript:void(0)">prev</a>`;
                            var next = `<a href="javascript:void(0)">next</a>`;
                            $('.paginationContainer').append(prev);
                            for(var i=0;i<response.paginations.batch_numpage;i++){
                                if(i==0){
                                    $('.paginationContainer').append(`<a href="javascript:void(0)" class="selected">${i+1}</a>`);  
                                }
                                else{
                                    $('.paginationContainer').append(`<a href="javascript:void(0)">${i+1}</a>`);
                                }
                                
                            }
                            $('.paginationContainer').append(next);
                            setPaginator();
                }
                else if (response.status == false) {
                    $("#error-msg").html(response.error[0]+" !");
                $('#error-dialogue').css("display","flex");
                }
                max_page = response.paginations.batch_numpage;
            },
            error: function(response){
                $("#error-msg").html("there is problem on serverside"+" !");
                $('#error-dialogue').css("display","none");
                $('#error-dialogue').css("display","flex");
            }
        });
});

function editDivision(attrId){
        
    var conditions = {};
    var paginations = {};
    conditions.id = attrId;
    var data = {};
    data.action="view";   
    data.conditions=JSON.stringify(conditions);
    data.paginations=JSON.stringify(paginations);
    $.ajax({
        url: BASE_SITE_URL + `/api/v1/auth/skill/`,
        type: "POST",
        // dataType: "json",
        data:data,
        success: function(response){
            if (response.status != false) {

                $('#edit_value').val(response.data.skill);
                jQuery('#editDivisionDialog').addClass('open');
                $('#editValueForm').on('submit',function(e){
                    e.preventDefault();
                    let conditions = $(this).serializeObject();
                        conditions.id = attrId;
                        let data = {};
                        data.action="update";   
                        data.conditions=JSON.stringify(conditions);
                    $.ajax({
                        url: BASE_SITE_URL + `/api/v1/auth/skill/`,
                        type: "POST",
                        // dataType: "json",
                        data:data,
                        success: function(response){
                            if (response.status != false) {
                                location.reload();
                            }
                            else if (response.status == false) {
                                jQuery('#editDivisionDialog').removeClass('open');
                                $("#error-msg").html(response.error[0]+" !");
                            $('#error-dialogue').css("display","flex");
                            }
                        },
                        error: function(response){
                            jQuery('#editDivisionDialog').removeClass('open');
                            $("#error-msg").html("there is problem on serverside"+" !");
                            $('#error-dialogue').css("display","none");
                            $('#error-dialogue').css("display","flex");
                        }
                    });
                })
            }
        }
    });
}

function removeDivision(attrId){
    var conditions = {};
    conditions.id = attrId;
    var data = {};
    data.action="remove";   
    data.conditions=JSON.stringify(conditions);
    $.ajax({
        url: BASE_SITE_URL + `/api/v1/auth/skill/`,
        type: "POST",
        // dataType: "json",
        data:data,
        success: function(response){
            if (response.status != false) {
                location.reload();
            }
        }
    });

}


function setPaginator(){
    $('#divPagination a').off('click');
    $('#divPagination a').on('click', function(e) {
    $('#divPagination a').removeClass('selected');
    var currBtn = e.target;
    $(currBtn).addClass('selected');
    if($(currBtn).html()=="prev"){
        if(page_count==1){
            page_count = 1;
        }
        else{
            page_count-=1;
        }
    }
    else if($(currBtn).html()=="next"){
        if(page_count == max_page){
            page_count=max_page;
        }
        else{
            page_count+=1;
        }
        
    }
    else{
        page_count = $(currBtn).html();
    }
    var department_count = 0;
    var conditions = {};
    var paginations = {};
    paginations.page = page_count;
    var data = {};
    data.action="view";   
    data.conditions=JSON.stringify(conditions);
    data.paginations = JSON.stringify(paginations);
    $.ajax({
            url: BASE_SITE_URL + `/api/v1/auth/skill/`,
            type: "POST",
            dataType: "json",
            data:data,
            success: function(response){
                if (response.status != false) {
                    $('.listingtable').empty();
                    for(var i=0;i<response.data.length;i++){
                        $('.listingtable').append(`<tr>
                        <td>${response.data[i].skill}</td>
                       <td>subject1</td>
                       <td><a href="javascript:void(0);" class='edit-link' onclick="editDivision(${response.data[i].id})"><i class="fa fa-pencil"></i></a><a href="javascript:void(0);" onclick="removeDivision(${response.data[i].id})"><i class="fa fa-trash"></i></a></td>
                    </tr>`);
                        department_count+=1;
                    }
                    $('#subject_count').html(department_count);
                    
                }
                
            }
        });
});
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

        // let tableData = [
        //     { id: '1', concepttitle: 'Electrostatic force', studenttitle: 'Physics'},
        //     { id: '2', concepttitle: 'Linear equations', studenttitle: 'Mathematics'},
        //     { id: '3', concepttitle: 'Thermodynamics', studenttitle: 'Chemistry'},
        //     { id: '4', concepttitle: 'Laws of motion', studenttitle: 'Physics'},
        //     { id: '5', concepttitle: 'Algebra', studenttitle: 'Mathematics'},
          
            
        // ]


        // let paginationData = [
        //     { id: '1', concepttitle: 'Electrostatic force', studenttitle: 'Physics'},
        //     { id: '2', concepttitle: 'Linear equations', studenttitle: 'Mathematics'},
        //     { id: '3', concepttitle: 'Thermodynamics', studenttitle: 'Chemistry'},
        //     { id: '4', concepttitle: 'Laws of motion', studenttitle: 'Physics'},
        //     { id: '5', concepttitle: 'Algebra', studenttitle: 'Mathematics'},
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

        

      
        // let tableHTML ='';
        // let paginationHTML ='';


        // tableData.forEach((val)=>{
        //     tableHTML += `<tr>
        //                <td>${val.concepttitle}</td>
        //                <td>${val.studenttitle}</td>
        //                <td><a href="javascript:void(0);" class='edit-link'><i class="fa fa-pencil"></i></a><a href="#"><i class="fa fa-trash"></i></a></td>
        //             </tr>`;

                    
        // });

        
        // jQuery('.listingtable').append(tableHTML);
        
       



        jQuery('#txt-search').keyup(function(e){
            let searchValue = $(this).val().toLowerCase();
                 console.log(searchValue);
                 console.log(tableData);
                 let getData = tableData.find(data => data.name === searchValue);
                 console.log(getData);
       
            });


       jQuery('.add-division-link').click(function(){
            //jQuery('.filter-section').css('display','flex');
            jQuery('.addDivisionDialog').addClass('open');
            jQuery('.addDivisionDialog.foredit').removeClass('open');

        });  

       jQuery('table td .edit-link').click(function(){
            //jQuery('.filter-section').css('display','flex');
            jQuery('.addDivisionDialog.foredit').addClass('open');
            

        });  

       $('#subjectdd, #editsubjectdd').selectpicker(); 

        jQuery('.addDivisionDialog .form-actions a').click(function(){
            jQuery('.addDivisionDialog').removeClass('open');
        });
        jQuery('.addDivisionDialog .form-actions a').click(function(){
            jQuery('.addDivisionDialog.foredit').removeClass('open');
        });
    

        $('#add-division').on('submit',function(e){
            e.preventDefault();
            var data = $(this).serializeObject();
            data["action"]="add";
            $.ajax({
                url: BASE_SITE_URL + `/api/v1/auth/skill/`,
                type: "POST",
                dataType: "json",
                data:data,
                success: function(response){
                    if (response.status != false) {
                        location.reload();
                      }
                      else if (response.status == false) {
                        jQuery('#addDivisionDialog').removeClass('open');
                        $("#error-msg").html(response.error[0]+" !");
                    $('#error-dialogue').css("display","flex");
                    }
                },
                error: function(response){
                    jQuery('#addDivisionDialog').removeClass('open');
                    $("#error-msg").html("there is problem on serverside"+" !");
                    $('#error-dialogue').css("display","none");
                    $('#error-dialogue').css("display","flex");
                }
            });
        });


    });


    /*
    conditions: {'departments': ['Sales', 'Marketing'], 'designation': ['Managers', 'Manager']}
    */