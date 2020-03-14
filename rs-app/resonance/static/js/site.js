//to hold the global level variables and functions
var BASE_SITE_URL = 'http://localhost:8000';

$('.edit-link').on('click',function(e){
    $('#dialogue_title').text("Edit");
})

$('span:contains("Add New")').on('click',function(e){
    $('#dialogue_title').text("Add");
})

$('button').css("background-color","rgb(185, 211, 76)");