var path= window.location.pathname.split("/");
var path_length = path.length-2
path1 = path[path_length]
var links=document.getElementsByTagName('a')
for (var i = 0; i<links.length; i++)
{
    if(path1=="subjects"){
        $('#classsubject_page').addClass("active");
        $('#subject_page').addClass("active");
        $(' aside .aside-container li.active').addClass('open').children('ul').show();
    }
    else{
      if(links[i].pathname.includes(path1)){
        links[i].parentNode.classList.add("active");
        if(links[i].parentNode.parentNode.parentNode.nodeName=="LI"){
          links[i].parentNode.parentNode.parentNode.classList.add("active");
          $(' aside .aside-container li.active').addClass('open').children('ul').show();
        }
    }
    else{
        if(["unit","chapter","topic","sub_topic"].includes(path1)){
            $('#classsubject_page').addClass("active");
            $('#subject_page').addClass("active");
            $(' aside .aside-container li.active').addClass('open').children('ul').show();
        }
    }
}
}
