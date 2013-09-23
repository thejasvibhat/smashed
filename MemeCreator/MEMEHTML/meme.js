
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
function reset()
{
    curColor = 0;
    curFontSize = 30;
    curfontFamily = "Arial";
    curfontWeight = "Normal";
    curfontStyle = "Normal";
}
var isDragging = false;
var i = 0;
var cuTextBox;
var curDemoBox;
var curColor = 0;
var curFontSize = 20;
var curfontFamily = "Arial";
var curfontWeight = "Normal";
var curfontStyle = "Normal";
var curImage;

function AddCaption()
{
    reset();
    i++;
    $("#BaseCanvas").append("<div class='demo"+i+"' style='width:200px;height:40px;x:0px;y:0px;position:absolute;top:250px;background-color:transparent;'><textarea  id='myText"+i+"' class='displayBlock' style='width:100%;height:100%;x:0px;y:0px;position:absolute;top:0; border-color:transparent;background-color:transparent;overflow:hidden;'>Add caption here</textarea></div>");  

    cuTextBox = $('#myText'+i+'');     

    ColorChanged(curColor);
    curFontSize = 20;
    FontSizeChange(curFontSize);
    UpdateFamily(curfontFamily);
    UpdateFontweight(curfontWeight);
    UpdateFontStyle(curfontStyle);
    var textBox = $('#myText'+i+'');
    var demoBox = $('.demo'+i+'');
    curDemoBox = demoBox;
    textBox.focus();
    demoBox.addClass("backgroundTransparent");
    textBox.mousedown(function down(ev){cuTextBox = textBox;isDragging = true;
                                        demoBox.removeClass("backgroundTransparent");});
  
   $("#BaseCanvas").mousemove(function moveall(event){
        
        if(isDragging)
        {
            
            curDemoBox.css("top",event.pageY - 30);
            curDemoBox.css("left",event.pageX - 40);
        }
   });
    demoBox.mouseup(function up(ev){curDemoBox = demoBox;isDragging = false;});
    demoBox.mousedown(function updown(ev){curDemoBox = demoBox;});
  
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
  $("#BaseCanvas").droppable({
      drop: function( event, ui ) {
          curImage =  $("#backImage");
          curImage.addClass('imagehide');
          var iconsrc = ui.draggable.find("img").context.src;
          var src = iconsrc.replace("icon","file");
         $("#backImage").attr('src', src);
      }
  });

  GetThumbnails();
});
function SelectCrop(div,selection)
{
    console.log(selection);
}
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
				    var test = '<div class="scrollableDiv" ><img class="widthCLass"  id="image_'+i+'"  src="'+$(this).text()+'"/></div>';                    
					var api = $(".scrollable").data("scrollable");
					api.addItem(test);
                    $( "#image_"+i+"" ).draggable({
                      revert: "invalid", // when not dropped, the item will revert back to its initial position
                      containment: "document",
                      helper: "clone",
                        start: function (e, ui) {
                        ui.helper.animate({
                            width: 120,
                            height: 120,
                        },0);
                    },
                        //cursorAt: {left:0, top:0},
                      cursor: "move",
                    zIndex:10000,
                    appendTo:$("#BaseCanvas")
                    });
                    $( "#image_"+i+"" ).load(function (){
                        
                        if((this.height) > (this.width))
                        {       
                             $(this).removeClass("widthCLass");
                            $(this).addClass("heightCLass");
                            
                        }
                        else
                        {
                            var margin = 'margin: '+(100 - this.height)/2+'px 0px 0px 0px;';                            
                            $(this).attr('style',margin);
                        }
                    });

				});
    });
	 
	
    return false;
}

function FontSizeChange(val)
{
    curFontSize = val;
    cuTextBox.css("font-size",val);
}
function UpdateFamily(val)
{
    curfontFamily = val;
    cuTextBox.css("font-family",val);
}
function UpdateFontweight(val)
{
    curfontWeight = val;
    cuTextBox.css("font-weight",val);
    
}
function UpdateFontStyle(val)
{
    curfontStyle = val;
    cuTextBox.css("font-style",val);
}
function ColorChanged(val)
{
    curColor = val;
     cuTextBox.css("color",val);
}
function Save()
{
    removeSelection();
}
function Crop()
{
     $('#BaseCanvas').imgAreaSelect({
        handles: true,
        onSelectEnd: SelectCrop
    });
    var xx1 = ($("#BaseCanvas").width() - curImage.width())/2;
    var yy1 = ($("#BaseCanvas").height() - curImage.height())/2;
    $('#BaseCanvas').imgAreaSelect({ x1: xx1, y1:yy1 , x2: xx1 + curImage.width() , y2: yy1 + curImage.height()});
}

function UpdateStepperUp()
{
    var targInput = $("#fontSizeText");
    var value = targInput.val();
    value++;
    var min = 20;
    var max = 100;
    if ((value > min)&&(value <= max))
        targInput.val(value);
    FontSizeChange(targInput.val());
}
function UpdateStepperDown()
{
    var targInput = $("#fontSizeText");
    var value = targInput.val();
    value--;
    var min = 20;
    var max = 100;
    if ((value < max)&&(value >= min))
        targInput.val(value);
    FontSizeChange(targInput.val());
}
function OnImageLoad()
{
    //alert($("#BaseCanvas").height());
    curImage = $("#backImage");
    curImage.removeClass('imagehide');
    if((curImage.height()) > (curImage.width()))
    {     
        curImage.removeClass("widthCLassImg");
        curImage.addClass("heightCLassImg");
              var margin = 'margin: 0px 0px 0px '+($("#BaseCanvas").width() - curImage.width())/2+'px;';                            
        curImage.attr('style',margin);
        
    }
    else
    {
                curImage.addClass("widthCLassImg");
        curImage.removeClass("heightCLassImg");

        var margin = 'margin: '+($("#BaseCanvas").height() - curImage.height())/2+'px 0px 0px 0px;';                            
        curImage.attr('style',margin);
    }
}
function removeSelection()
{
    $('#BaseCanvas').imgAreaSelect({remove:true});
}