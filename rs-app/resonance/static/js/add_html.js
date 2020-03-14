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
function success(){
    window.location='/user/faculties/';
}

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#front_image')
                .attr('src', e.target.result)
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$(window).on('load',function(){

    $.ajax({
            url:`/institute/csc_finder?type=1`,
            type: "GET",
            dataType: "json",
            success: function(response){
                if (response.status != false) {
                    $('#country-getting-started').empty();
                    $('#country-getting-started').append(`<option value="" selected disabled>Select Country</option>`);
                    for(var i=0;i<response.data.length;i++){
                        $('#country-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].label}</option>`);
                    }
                    $(`select[id="country-getting-started"] option[value="${$('#country_id').val()}"]`).attr('selected', 'selected');
                    //$('#country-getting-started').selectpicker('refresh'); 
            }
        }
           
        });


        $.ajax({
            url:`/institute/csc_finder?type=2&parent=${$('#country_id').val()}`,
            type: "GET",
            dataType: "json",
            success: function(response){
                if (response.status != false) {
                    $('#state-getting-started').empty();
                    $('#state-getting-started').append(`<option value="" selected disabled>Select State</option>`);
                    $('#city-getting-started').empty();
                    $('#city-getting-started').append(`<option value="" selected disabled>Select City</option>`);
                    for(var i=0;i<response.data.length;i++){
                        $('#state-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].label}</option>`);
                    }
                    $(`select[id="state-getting-started"] option[value="${$('#state_id').val()}"]`).attr('selected', 'selected');
                    //$('#state-getting-started').selectpicker('refresh'); 
            }
        }
           
        });

        $.ajax({
            url:`/institute/csc_finder?type=3&parent=${$('#state_id').val()}`,
            type: "GET",
            dataType: "json",
            success: function(response){
                if (response.status != false) {
                    $('#city-getting-started').empty();
                    $('#city-getting-started').append(`<option value="" selected disabled>Select City</option>`);
                    for(var i=0;i<response.data.length;i++){
                        $('#city-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].label}</option>`);
                    }
                    $(`select[id="city-getting-started"] option[value="${$('#city_id').val()}"]`).attr('selected', 'selected');
                   // $('#city-getting-started').selectpicker('refresh'); 
            }
        }
           
        });

        $.ajax({
            url:`/institute/center_finder?parent=${$('#city_id').val()}`,
            type: "GET",
            dataType: "json",
            success: function(response){
              
                if (response.status != false) {
                    $('#center-getting-started').empty();
                    $('#center-getting-started').append(`<option value="" selected disabled>Select Center</option>`);
                    for(var i=0;i<response.data.length;i++){
                        $('#center-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);
                    }
                    $(`select[id="center-getting-started"] option[value="${$('#center_id').val()}"]`).attr('selected', 'selected');
                    //$('#center-getting-started').selectpicker('refresh'); 
            }
        }
           
        });


    });

  function SelectState(){
    var selected_country =$( "#country-getting-started option:selected" ).val();
    $.ajax({
        url:`/institute/csc_finder?type=2&parent=${selected_country}`,
        type: "GET",
        dataType: "json",
        success: function(response){
            if (response.status != false) {
                $('#state-getting-started').empty();
                $('#state-getting-started').append(`<option value="" selected disabled>Select State</option>`);
                $('#city-getting-started').empty();
                $('#city-getting-started').append(`<option value="" selected disabled>Select City</option>`);
                for(var i=0;i<response.data.length;i++){
                    $('#state-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].label}</option>`);
                    
                }
                //$('#state-getting-started').selectpicker('refresh');
        }
    }
       
    });
}

function SelectCity(){
  var selected_state =$( "#state-getting-started option:selected" ).val();
  $.ajax({
      url:`/institute/csc_finder?type=3&parent=${selected_state}`,
      type: "GET",
      dataType: "json",
      success: function(response){
          if (response.status != false) {
              $('#city-getting-started').empty();
              $('#city-getting-started').append(`<option value="" selected disabled>Select City</option>`);
              for(var i=0;i<response.data.length;i++){
                  $('#city-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].label}</option>`);
                  
              }
             // $('#city-getting-started').selectpicker('refresh');
      }
  }
     
  });
}

function SelectCenter(){
  var selected_state =$( "#city-getting-started option:selected" ).val();
  $.ajax({
      url:`/institute/center_finder?parent=${selected_state}`,
      type: "GET",
      dataType: "json",
      success: function(response){
          if (response.status != false) {
              $('#center-getting-started').empty();
              $('#center-getting-started').append(`<option value="" selected disabled>Select Center</option>`);
              for(var i=0;i<response.data.length;i++){
                  $('#center-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);
                  
              }
              //$('#center-getting-started').selectpicker('refresh');
      }
  }
     
  });
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

    $('.successDialog').css("display","flex");

    
    //$('#subject_list').selectpicker(); 
    //$('#batches-getting-started').selectpicker();
    //$('#country-getting-started').selectpicker();  
    //$('#center-getting-started').selectpicker();
    $('#region-getting-started').selectpicker();
    $('#skill-getting-started').selectpicker();
    //$('#state-getting-started').selectpicker();
    //$('#city-getting-started').selectpicker();
    //$('#division-getting-started').selectpicker();
    $('#designation-getting-started').selectpicker();
    $('#et-getting-started').selectpicker();
    //$('#department-getting-started').selectpicker();

    
    $(`select[name="department"] option[value="${$('#department_id').val()}"]`).attr('selected', 'selected');
      //$('#department-getting-started').selectpicker('refresh');
      $(`select[name="designation"] option[value="${$('#designation_id').val()}"]`).attr('selected', 'selected');
      $('#designation-getting-started').selectpicker('refresh');
      $(`select[name="division"] option[value="${$('#division_id').val()}"]`).attr('selected', 'selected');
      //$('#division-getting-started').selectpicker('refresh');
      $(`select[name="employement_type"] option[value="${$('#employement_type_id').val()}"]`).attr('selected', 'selected');
      $('#et-getting-started').selectpicker('refresh');
      $(`select[name="role"] option[value="${$('#role_id').val()}"]`).attr('selected', 'selected');
      $(`select[id="reporting-manager"] option[value="${$('#reporting_income').val()}"]`).attr('selected', 'selected');
      var subject_list=$('#subject_id').val().split("");
      var batch_list=$('#batch_id').val().split("");
      for(var i in subject_list){
        $(`select[name="subject"] option[value="${subject_list[i]}"]`).attr('selected', 'selected');
        //$('#subject_list').selectpicker('refresh');   
      }
      for(var i in batch_list){
        $(`select[name="batch"] option[value="${batch_list[i]}"]`).attr('selected', 'selected');
        //$('#batches-getting-started').selectpicker('refresh');   
      }
     
  });

function reporting()
{
 
  var reporting = $('#reporting').val()
  var dataString = {"reporting_man":reporting}
  
   // $.ajax({
   //      url:  '/user/reporting_man/',
   //      type: "GET",
   //      dataType: "json",
   //      data:dataString,
   //      success: function(response){
   //        alert(JSON.stringify(response))
          
        
           
           
           
   //      }
   //  })
}