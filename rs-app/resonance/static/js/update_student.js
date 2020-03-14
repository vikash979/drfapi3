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

  function success(){
    window.location='/user/student_listing/';
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
                        $('#country-getting-started').selectpicker('refresh');
                    }
                    $(`select[name="country"] option[value="${$('#country_id').val()}"]`).attr('selected', 'selected');
                    $('#country-getting-started').selectpicker('refresh'); 
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
                        $('#state-getting-started').selectpicker('refresh');
                    }
                    $(`select[name="state"] option[value="${$('#state_id').val()}"]`).attr('selected', 'selected');
                    $('#state-getting-started').selectpicker('refresh'); 
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
                        $('#city-getting-started').selectpicker('refresh');
                    }
                    $(`select[name="city"] option[value="${$('#city_id').val()}"]`).attr('selected', 'selected');
                    $('#city-getting-started').selectpicker('refresh'); 
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
                        $('#center-getting-started').selectpicker('refresh');
                    }
                    $(`select[name="center"] option[value="${$('#center_id').val()}"]`).attr('selected', 'selected');
                    $('#center-getting-started').selectpicker('refresh'); 
            }
        }
           
        });
       
        $(`select[name="session"] option[value="${$('#session_id').val()}"]`).attr('selected', 'selected');
        var session_id = $('#session').val()
        dataString = {"session_id":session_id}
            $.ajax({
                url:  '/user/program_session/',
                type: "GET",
                dataType: "json",
                data:dataString,
                success: function(response){
                  var phase_ob = response.sub_data;
                  $('#program').empty()
                  $('#program').append(`<option selected disabled> Select Program </option>`)
                  for (var i=0; i<Object.keys(phase_ob).length;i++) 
                    {   
                      $('#program').append(`<option value="${phase_ob[Object.keys(phase_ob)[i]][0]}"> ${phase_ob[Object.keys(phase_ob)[i]][1]} </option>`);
                    }
                    $(`select[name="program"] option[value="${$('#program_id').val()}"]`).attr('selected', 'selected');
                }
            })
          var program_id = $('#program_id').val()
          var session_id = $('#session').val();
            dataString = {"session_id":session_id,"program_id":program_id}
                $.ajax({
                  url:  '/user/program_phase_session/',
                  type: "GET",
                  dataType: "json",
                  data:dataString,
                  success: function(response){
                      var phase_ob = response.sub_data;
                      $('#phase').empty()
                      $('#phase').append(`<option selected disabled> Select Phase </option>`)
                    for (var i=0; i<Object.keys(phase_ob).length;i++) 
                      {   
                        $('#phase').append(`<option value="${phase_ob[Object.keys(phase_ob)[i]][0]}"> ${phase_ob[Object.keys(phase_ob)[i]][1]} </option>`);
                      }
                      $(`select[name="phase"] option[value="${$('#phase_id').val()}"]`).attr('selected', 'selected');
                  }
              })
            var program_id = $('#program_id').val()
            var session_id = $('#session').val()
            if (program_id!='')
                {
                  dataString = {"program_id":program_id}
                  $.ajax({
                    url:  '/user/program_class/',
                    type: "GET",
                    dataType: "json",
                    data:dataString,
                    success: function(response){
                    var class_ob = response['sub_data']
                      $('#class').empty()
                      $('#class').append(`<option selected disabled>Select Class</option>`)
                      for (var i=0; i<class_ob.length;i++) 
                        {
                      
                        $('#class').append(`<option value="${class_ob[i]['class_id']}">${class_ob[i]['class_label']}</option>`);
                        }
                        $(`select[name="class"] option[value="${$('#class_id').val()}"]`).attr('selected', 'selected');
                    }
                })
              }
          var phase_id = $('#phase_id').val()
          dataString = {"phase_id":phase_id}
            $.ajax({
              url:  '/user/batch_phase/',
              type: "GET",
              dataType: "json",
              data:dataString,
              success: function(response){
                
                var class_ob = response['sub_data'];
                $('#current_batch').empty()
                $('#current_batch').append(`<option selected disabled>Select Batch</option>`)
                for (var i=0; i<class_ob.length;i++) 
                  {
                  $('#current_batch').append(`<option value="${class_ob[i]['id']}">${class_ob[i]['label']}</option>`);
                  }
                  $(`select[name="current_batch"] option[value="${$('#batch_id').val()}"]`).attr('selected', 'selected');
                
              }
          })
          

          






    //window load ends......    
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
                      $('#state-getting-started').selectpicker('refresh');
                  }
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
                    $('#city-getting-started').selectpicker('refresh');
                }
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
          console.log(response);
            if (response.status != false) {
                $('#center-getting-started').empty();
                $('#center-getting-started').append(`<option value="" selected disabled>Select Center</option>`);
                for(var i=0;i<response.data.length;i++){
                    $('#center-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);
                    $('#center-getting-started').selectpicker('refresh');
                }
        }
    }
       
    });
  }
  
  
  
  function success(){
    window.location = `/user/student_listing/`;
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
    //$('#region-getting-started').selectpicker();
    //$('#skill-getting-started').selectpicker();
    //$('#state-getting-started').selectpicker();
    //$('#city-getting-started').selectpicker();
    //$('#division-getting-started').selectpicker();
    //$('#designation-getting-started').selectpicker();
    //$('#et-getting-started').selectpicker();
    //$('#department-getting-started').selectpicker();
    //$('#phase').selectpicker();
    //$('#session').selectpicker();
    //$('#program').selectpicker();
    //$('#gender').selectpicker();
    //$('#medium').selectpicker();
    //$('#divisionFilter').selectpicker();
       
      $(`select[name="division"] option[value="${$('#division_id').val()}"]`).attr('selected', 'selected');
      //$('#division').selectpicker('refresh');
      $(`select[name="gender"] option[value="${$('#gender_id').val()}"]`).attr('selected', 'selected');
      //$('#gender').selectpicker('refresh');
      $(`select[name="medium"] option[value="${$('#medium_id').val()}"]`).attr('selected', 'selected');
      //$('#medium').selectpicker('refresh');
      // $(`select[name="phase"] option[value="${$('#phase_id').val()}"]`).attr('selected', 'selected');
      //$('#phase').selectpicker('refresh');
      // $(`select[name="session"] option[value="${$('#session_id').val()}"]`).attr('selected', 'selected');
      // $('#session').selectpicker('refresh');
      // $(`select[name="class"] option[value="${$('#class_id').val()}"]`).attr('selected', 'selected');
     // $('#class').selectpicker('refresh');
      // $(`select[name="program"] option[value="${$('#program_id').val()}"]`).attr('selected', 'selected');
      //$('#program').selectpicker('refresh');
      
    });
  

    function program_session()
    {
      $('#program').empty();
      $('#phase').empty();
      $('#current_batch').empty();
      $('#class').empty();
      var session_id = $('#session').val()
        dataString = {"session_id":session_id}
       $.ajax({
          url:  '/user/program_session/',
          type: "GET",
          dataType: "json",
          data:dataString,
          success: function(response){
             var phase_ob = response.sub_data;
             $('#program').empty()
             $('#program').append(`<option selected disabled> Select Program </option>`)
            for (var i=0; i<Object.keys(phase_ob).length;i++) 
              {   
                $('#program').append(`<option value="${phase_ob[Object.keys(phase_ob)[i]][0]}"> ${phase_ob[Object.keys(phase_ob)[i]][1]} </option>`);
              }
  
          }
      })
      
    }
  
    function program_phase_session()
    {
      var program_id = $('#program').val();
      var session_id = $('#session').val();
        dataString = {"session_id":session_id,"program_id":program_id}
       $.ajax({
          url:  '/user/program_phase_session/',
          type: "GET",
          dataType: "json",
          data:dataString,
          success: function(response){
             var phase_ob = response.sub_data;
             $('#phase').empty()
             $('#phase').append(`<option selected disabled> Select Phase </option>`)
            for (var i=0; i<Object.keys(phase_ob).length;i++) 
              {   
                $('#phase').append(`<option value="${phase_ob[Object.keys(phase_ob)[i]][0]}"> ${phase_ob[Object.keys(phase_ob)[i]][1]} </option>`);
              }
  
          }
      })
      
    }
  
  
    function program_class()
    {
      $('#phase').empty();
    $('#current_batch').empty();
    $('#class').empty();
      var program_id = $('#program').val()
      var session_id = $('#session').val()
      if (program_id!='')
      {
        dataString = {"program_id":program_id}
        $.ajax({
          url:  '/user/program_class/',
          type: "GET",
          dataType: "json",
          data:dataString,
          success: function(response){
           var class_ob = response['sub_data']
             $('#class').empty()
             $('#class').append(`<option selected disabled>Select Class</option>`)
            for (var i=0; i<class_ob.length;i++) 
              {
             
               $('#class').append(`<option value="${class_ob[i]['class_id']}">${class_ob[i]['class_label']}</option>`);
              }
           
          }
      })
      }
    }
  
    function phase_batch()
    {
    $('#current_batch').empty();
      var phase_id = $('#phase').val()
      dataString = {"phase_id":phase_id}
        $.ajax({
          url:  '/user/batch_phase/',
          type: "GET",
          dataType: "json",
          data:dataString,
          success: function(response){
            
           var class_ob = response['sub_data'];
            $('#current_batch').empty()
            $('#current_batch').append(`<option selected disabled>Select Batch</option>`)
            for (var i=0; i<class_ob.length;i++) 
              {
              $('#current_batch').append(`<option value="${class_ob[i]['id']}">${class_ob[i]['label']}</option>`);
              }
           
          }
      })
  
  
    }