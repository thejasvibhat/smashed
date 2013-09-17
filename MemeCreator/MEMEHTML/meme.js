
function ChangeBackground()
{
    $("#myFile").click();    
    $('#myFile').change(function(input)
    {
        
        var file = input.target.files[0];
        var reader = new FileReader();

        reader.readAsDataURL(file);
        reader.onloadend = function(e) {
            $("#backImage").attr('src', e.target.result);  
        } 

            
        
    });  
}
var isDragging = false;
var i = 0;
var cuTextBox;
var curColor = 0;
var curFontSize = 30;
function AddCaption()
{
    i++;
    $("#BaseCanvas").append("<div class='demo"+i+" ui-widget-content' style='width:200px;height:40px;x:0px;y:0px;position:absolute;top:200px'><input type='text'  id='myText"+i+"' class='displayBlock' value='caption' style='width:100%;height:100%;x:0px;y:0px;position:absolute;top:0; border-color:transparent;background-color:transparent;font-size:20px;'></div>");  
    $('.demo'+i+'').resizable();
    $('.demo'+i+'').draggable();
    cuTextBox = $('.demo'+i+'');     
    ColorChanged(curColor);
    FontSizeChange(curFontSize);
    var textBox = $('#myText'+i+'');
    var demoBox = $('.demo'+i+'');
    textBox.mousedown(function down(ev){cuTextBox = textBox;isDragging = true;  textBox.addClass("pointerNone");});
    textBox.focusout(function(){
        textBox.removeClass("pointerNone");
    });

   } 


function Apply()
{

    var fontsize = $("#fontsize").val() + 'px';
    cuTextBox.css("font-size",fontsize);
}

$(function() {
  // initialize scrollable
  $('#color1').colorPicker();
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

function DropMeme(ev)
{
    var data=ev.dataTransfer.getData("Text");
    $("#backImage").attr('src', data);
    ev.preventDefault();
}
function DragMeme(ev)
{
    
    ev.dataTransfer.setData("Text",ev.target.src);
}
function allowDrop(ev)
{
ev.preventDefault();
}
function FontSizeChange(val)
{
    curFontSize = val;
    cuTextBox.css("font-size",val);
}

function ColorChanged(val)
{
    curColor = val;
     cuTextBox.css("color",val);
}