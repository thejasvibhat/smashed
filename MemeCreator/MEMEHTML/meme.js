
function ChangeBackground()
{
    $("#myFile").click();    
    $('#myFile').change(function(input)
    {
        
        var file = input.target.files[0];
        var reader = new FileReader();

        reader.readAsDataURL(file);
        reader.onloadend = function(e) {
            $("#image").attr('src', e.target.result);  
        } 

            
        
    });  
}
var isDragging = false;
var i = 0;
var cuTextBox;
function AddCaption()
{
    i++;
    $("#BaseCanvas").append("<div class='demo"+i+"' style='width:200px;height:40px;x:0px;y:0px;position:absolute;top:100px'><input type='text'  id='myText"+i+"' class='displayBlock' style='width:100%;height:100%;x:0px;y:0px;position:absolute;top:0; border-color:transparent;background-color:transparent;font-size:40px'></div>");  
 $('.demo'+i+'').resizable();
    applyMovement(i); 
    

   } 

function applyMovement(i){
    var textBox = $('#myText'+i+'');
    var demoBox = $('.demo'+i+'');
        textBox.mousedown(function down(){cuTextBox = textBox; isDragging = true;demoBox.trigger('mousedown');});
    textBox.mouseup(function up(){isDragging = false;demoBox.trigger('mouseup');});
    $("#myText").mousemove(function move(){demoBox.trigger('mousemove');});
    demoBox.mousemove(function moveall(event){
        
        if(isDragging)
        {
            
            demoBox.css("top",event.pageY - 30);
            demoBox.css("left",event.pageX - 30);
        }
    });
}
function Apply()
{

    var fontsize = $("#fontsize").val() + 'px';
    cuTextBox.css("font-size",fontsize);
}

$(function() {
  // initialize scrollable
 
  $(".scrollable").scrollable();
  GetThumbnails();
});
function GetThumbnails()
{
    $.ajax({
        url: "/actions/list",
        type: 'GET',
        crossDomain: true,

        
    }).done(function ( data ) {
               theXmlDoc = $.parseXML(data);
			   var theRow = $(theXmlDoc).find('url').get();
			   $(theRow).each(function(i) 
				{
				    var test = '<img src="'+$(this).text()+'"/>';
					var api = $(".scrollable").data("scrollable");
					api.addItem(test);
				});
    });
	 
	
    return false;
}

