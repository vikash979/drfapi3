
$(window).on('load',function(){
    var d = new Date();
    var n = d.getFullYear(n)
    var i =2010;
    for (var i =2015;i<=n;i++)
    {
    
    $('#year').append(`<option value="${i}" selected="selected">${i}</option>`);
    $('#years').append(`<option value="${i}" selected="selected">${i}</option>`);
    }
})
  function openPopup(){
      $('#openPopUp').addClass('open');
  }
  
  
  
  //////////////////////////////////////////////
  
  // function session_obj(sessionId)
  // {
  //     $.ajax({
  //         url: BASE_SITE_URL + '/api/v1/institute/sessions/',
  //         type: "POST",
  //         dataType: "json",
  //         data:{"action":"view"},
  //         success: function(response){
  //             $('#total_session').text(response.data.length)
  //             //alert(JSON.stringify(response.data))
              
  //             if (response.data.length > 0)
  //             {
  //                 for(var i=0;i<response.data.length;i++){
  //                    // alert(response.data)
  //                // $('#listingtable').append(`<tr> <td>    ${response.data[i].display_name}</td><td>${response.data[i].name}</td><td>${response.data[i].description}</td><td></td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href="#" onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`)
  //                 }
  
  //             }
  //             else{
  //                 //$('#listingtable').append(`<tr> <td colspan="4">There is no record</td></tr>`)
  //             }
  
              
                   
             
  //         }
  //     })
  // }