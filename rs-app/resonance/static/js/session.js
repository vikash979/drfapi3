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


//////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
///////////////////////////////////////////////////
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
    // { id: '1', concepttitle: 'Electrostatic force', studenttitle: 'Physics'},
    // { id: '2', concepttitle: 'Linear equations', studenttitle: 'Mathematics'},
    // { id: '3', concepttitle: 'Thermodynamics', studenttitle: 'Chemistry'},
    // { id: '4', concepttitle: 'Laws of motion', studenttitle: 'Physics'},
    // { id: '5', concepttitle: 'Algebra', studenttitle: 'Mathematics'},
  
    
]


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




let tableHTML ='';
let paginationHTML ='';


tableData.forEach((val)=>{
    tableHTML += `<tr>
               <td>${val.concepttitle}</td>
               <td>${val.studenttitle}</td>
               <td><a href="javascript:void(0);" class='edit-link'><i class="fa fa-pencil"></i></a><a href="#"><i class="fa fa-trash"></i></a></td>
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



});










var input = document.querySelector('input[name="input-custom-dropdown"]'),
// init Tagify script on the above inputs
tagify = new Tagify(input, {
whitelist: ["A# .NET", "A# (Axiom)", "A-0 System", "A+", "A++", "ABAP", "ABC", "ABC ALGOL", "ABSET", "ABSYS", "ACC", "Accent", "Ace DASL", "ACL2", "Avicsoft", "ACT-III", "Action!", "ActionScript", "Ada", "Adenine", "Agda", "Agilent VEE", "Agora", "AIMMS", "Alef", "ALF", "ALGOL 58", "ALGOL 60", "ALGOL 68", "ALGOL W", "Alice", "Alma-0", "AmbientTalk", "Amiga E", "AMOS", "AMPL", "Apex (Salesforce.com)", "APL", "AppleScript", "Arc", "ARexx", "Argus", "AspectJ", "Assembly language", "ATS", "Ateji PX", "AutoHotkey", "Autocoder", "AutoIt", "AutoLISP / Visual LISP", "Averest", "AWK", "Axum", "Active Server Pages", "ASP.NET", "B", "Babbage", "Bash", "BASIC", "bc", "BCPL", "BeanShell", "Batch (Windows/Dos)", "Bertrand", "BETA", "Bigwig", "Bistro", "BitC", "BLISS", "Blockly", "BlooP", "Blue", "Boo", "Boomerang", "Bourne shell (including bash and ksh)", "BREW", "BPEL", "B", "C--", "C++ – ISO/IEC 14882", "C# – ISO/IEC 23270", "C/AL", "Caché ObjectScript", "C Shell", "Caml", "Cayenne", "CDuce", "Cecil", "Cesil", "Céu", "Ceylon", "CFEngine", "CFML", "Cg", "Ch", "Chapel", "Charity", "Charm", "Chef", "CHILL", "CHIP-8", "chomski", "ChucK", "CICS", "Cilk", "Citrine (programming language)", "CL (IBM)", "Claire", "Clarion", "Clean", "Clipper", "CLIPS", "CLIST", "Clojure", "CLU", "CMS-2", "COBOL – ISO/IEC 1989", "CobolScript – COBOL Scripting language", "Cobra", "CODE", "CoffeeScript", "ColdFusion", "COMAL", "Combined Programming Language (CPL)", "COMIT", "Common Intermediate Language (CIL)", "Common Lisp (also known as CL)", "COMPASS", "Component Pascal", "Constraint Handling Rules (CHR)", "COMTRAN", "Converge", "Cool", "Coq", "Coral 66", "Corn", "CorVision", "COWSEL", "CPL", "CPL", "Cryptol", "csh", "Csound", "CSP", "CUDA", "Curl", "Curry", "Cybil", "Cyclone", "Cython", "Java", "Javascript", "M2001", "M4", "M#", "Machine code", "MAD (Michigan Algorithm Decoder)", "MAD/I", "Magik", "Magma", "make", "Maple", "MAPPER now part of BIS", "MARK-IV now VISION:BUILDER", "Mary", "MASM Microsoft Assembly x86", "MATH-MATIC", "Mathematica", "MATLAB", "Maxima (see also Macsyma)", "Max (Max Msp – Graphical Programming Environment)", "Maya (MEL)", "MDL", "Mercury", "Mesa", "Metafont", "Microcode", "MicroScript", "MIIS", "Milk (programming language)", "MIMIC", "Mirah", "Miranda", "MIVA Script", "ML", "Model 204", "Modelica", "Modula", "Modula-2", "Modula-3", "Mohol", "MOO", "Mortran", "Mouse", "MPD", "Mathcad", "MSIL – deprecated name for CIL", "MSL", "MUMPS", "Mystic Programming L"],
maxTags: 10,
dropdown: {
maxItems: 20,           // <- mixumum allowed rendered suggestions
classname: "tags-look", // <- custom classname for this dropdown, so it could be targeted
enabled: 0,             // <- show suggestions on focus
closeOnSelect: false    // <- do not hide the suggestions dropdown once an item has been selected
}
}) 



$( "form" ).on( "submit", function( event ) {
    event.preventDefault();
    console.log( $( this ).serializeArray() );
  });

var input = document.querySelector('input[name="input-custom-dropdown"]'),
// init Tagify script on the above inputs
tagify = new Tagify(input, {
whitelist: ["A# .NET", "A# (Axiom)", "A-0 System", "A+", "A++", "ABAP", "ABC", "ABC ALGOL", "ABSET", "ABSYS", "ACC", "Accent", "Ace DASL", "ACL2", "Avicsoft", "ACT-III", "Action!", "ActionScript", "Ada", "Adenine", "Agda", "Agilent VEE", "Agora", "AIMMS", "Alef", "ALF", "ALGOL 58", "ALGOL 60", "ALGOL 68", "ALGOL W", "Alice", "Alma-0", "AmbientTalk", "Amiga E", "AMOS", "AMPL", "Apex (Salesforce.com)", "APL", "AppleScript", "Arc", "ARexx", "Argus", "AspectJ", "Assembly language", "ATS", "Ateji PX", "AutoHotkey", "Autocoder", "AutoIt", "AutoLISP / Visual LISP", "Averest", "AWK", "Axum", "Active Server Pages", "ASP.NET", "B", "Babbage", "Bash", "BASIC", "bc", "BCPL", "BeanShell", "Batch (Windows/Dos)", "Bertrand", "BETA", "Bigwig", "Bistro", "BitC", "BLISS", "Blockly", "BlooP", "Blue", "Boo", "Boomerang", "Bourne shell (including bash and ksh)", "BREW", "BPEL", "B", "C--", "C++ – ISO/IEC 14882", "C# – ISO/IEC 23270", "C/AL", "Caché ObjectScript", "C Shell", "Caml", "Cayenne", "CDuce", "Cecil", "Cesil", "Céu", "Ceylon", "CFEngine", "CFML", "Cg", "Ch", "Chapel", "Charity", "Charm", "Chef", "CHILL", "CHIP-8", "chomski", "ChucK", "CICS", "Cilk", "Citrine (programming language)", "CL (IBM)", "Claire", "Clarion", "Clean", "Clipper", "CLIPS", "CLIST", "Clojure", "CLU", "CMS-2", "COBOL – ISO/IEC 1989", "CobolScript – COBOL Scripting language", "Cobra", "CODE", "CoffeeScript", "ColdFusion", "COMAL", "Combined Programming Language (CPL)", "COMIT", "Common Intermediate Language (CIL)", "Common Lisp (also known as CL)", "COMPASS", "Component Pascal", "Constraint Handling Rules (CHR)", "COMTRAN", "Converge", "Cool", "Coq", "Coral 66", "Corn", "CorVision", "COWSEL", "CPL", "CPL", "Cryptol", "csh", "Csound", "CSP", "CUDA", "Curl", "Curry", "Cybil", "Cyclone", "Cython", "Java", "Javascript", "M2001", "M4", "M#", "Machine code", "MAD (Michigan Algorithm Decoder)", "MAD/I", "Magik", "Magma", "make", "Maple", "MAPPER now part of BIS", "MARK-IV now VISION:BUILDER", "Mary", "MASM Microsoft Assembly x86", "MATH-MATIC", "Mathematica", "MATLAB", "Maxima (see also Macsyma)", "Max (Max Msp – Graphical Programming Environment)", "Maya (MEL)", "MDL", "Mercury", "Mesa", "Metafont", "Microcode", "MicroScript", "MIIS", "Milk (programming language)", "MIMIC", "Mirah", "Miranda", "MIVA Script", "ML", "Model 204", "Modelica", "Modula", "Modula-2", "Modula-3", "Mohol", "MOO", "Mortran", "Mouse", "MPD", "Mathcad", "MSIL – deprecated name for CIL", "MSL", "MUMPS", "Mystic Programming L"],
maxTags: 10,
dropdown: {
  maxItems: 20,           // <- mixumum allowed rendered suggestions
  classname: "tags-look", // <- custom classname for this dropdown, so it could be targeted
  enabled: 0,             // <- show suggestions on focus
  closeOnSelect: false    // <- do not hide the suggestions dropdown once an item has been selected
}
}) 


