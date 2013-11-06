function UploadSkeleton()
{
    
}
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
            UploadSkeleton();
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
var curImageId;
var m_arrTextBoxes = new Array();
var m_arrDemoBoxes = new Array();
var curSelectionX = 0;
var curSelectionY = 0;
var curSelectionWidth = 1;
var curSelectionHeight = 1;
function AddCaption()
{
    reset();
    i++;
    var top = 250;
    if(i== 1)
        top = 300;
    else if(i == 2)
        top = 650;
        
        
    $("#BaseCanvas").append("<div class='demo"+i+"' style='width:200px;height:40px;x:0px;y:0px;position:absolute;left:320px;top:"+top+"px;background-color:transparent;'><textarea  id='myText"+i+"' class='displayBlock' style='width:100%;height:100%;x:0px;y:0px;position:absolute;top:0; border-color:transparent;background-color:transparent;overflow:hidden;'>Add caption here</textarea></div>");  
    
    cuTextBox = $('#myText'+i+'');     
m_arrTextBoxes.push(cuTextBox);
    ColorChanged(curColor);
    curFontSize = 20;
    FontSizeChange(curFontSize);
    UpdateFamily(curfontFamily);
    UpdateFontweight(curfontWeight);
    UpdateFontStyle(curfontStyle);
    var textBox = $('#myText'+i+'');
    var demoBox = $('.demo'+i+'');
    m_arrDemoBoxes.push(demoBox);
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
          var value =    iconsrc.split("?")[1];
          value = value.substring(3); 

         $("#backImage").attr('src', src);
          
          $("#backImage").attr('value', value);
      }
  });

  GetThumbnails();
});
function SelectCrop(div,selection)
{
    curSelectionX = selection.x1/450;
    curSelectionY = selection.y1/450;
    curSelectionWidth = selection.x2/450;
    curSelectionHeight = selection.y2/450;
}
function GetThumbnails()
{
    $.ajax({
        url: "/meme/actions/list",
        type: 'GET',
        crossDomain: true,

        
    }).done(function ( data ) {
               theXmlDoc = $.parseXML(data);
			   var theRow = $(theXmlDoc).find('url').get();
			   $(theRow).each(function(i) 
				{
				    var test = '<div class="scrollableDiv" ><img class="widthCLass" id="image_'+i+'"  src="'+$(this).text()+'"/></div>';                    
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
    var xmlDocument = $.parseXML("<root/>");
    var oObjetcs = document.createElement('objects')
    
    oObjetcs.setAttribute("x",curSelectionX);
    oObjetcs.setAttribute("y",curSelectionY);
    oObjetcs.setAttribute("width",curSelectionWidth);
    oObjetcs.setAttribute("height",curSelectionHeight);
    
    var oImages = document.createElement('image')
    oImages.setAttribute("id",curImage.val());
    oImages.setAttribute("width",curImage.width());
    oImages.setAttribute("height",curImage.height());
    var oTextBoxes = document.createElement('texts')
    for(var i=0; i < m_arrTextBoxes.length ; i++)
    {
        var oTextXml = xmlDocument.createElement('text');        
        var oTextBox = m_arrTextBoxes[i];
        var oProperty = xmlDocument.createElement('properties');
        oProperty.setAttribute("size",oTextBox.css("font-size").split("p")[0]);
        oProperty.setAttribute("color",oTextBox.css("color"));
        oProperty.setAttribute("style",oTextBox.css("font-style"));
        oProperty.setAttribute("weight",oTextBox.css("font-weight"));
        oProperty.setAttribute("name",oTextBox.css("font-family"));
        oProperty.setAttribute("left",m_arrDemoBoxes[i].css("left").split("p")[0] - $("#BaseCanvas").position().left);
        oProperty.setAttribute("top",m_arrDemoBoxes[i].css("top").split("p")[0] - $("#BaseCanvas").position().top);
        oProperty.setAttribute("width",oTextBox.width());
        oProperty.setAttribute("height",oTextBox.height());
        oProperty.setAttribute("textVal",oTextBox.val());
        oTextXml.appendChild(oProperty);
        oTextBoxes.appendChild(oTextXml);
        
    }
    oObjetcs.appendChild(oTextBoxes);
    oObjetcs.appendChild(oImages);
    xmlDocument.documentElement.appendChild(oObjetcs);
    $.ajax({
      type: "POST",
      crossDomain: true,
      url: '/meme/actions/save',
        data : {
            method : "Save",
            data : XMLToString(xmlDocument)
        },

    }).done(function ( datanew ) {
        window.location.href = '/meme/index.html';
        //alert(datanew);
    });
}
function XMLToString(oXML)
{
 //code for IE
 if (window.ActiveXObject) {
 var oString = oXML.xml; return oString;
 } 
 // code for Chrome, Safari, Firefox, Opera, etc.
 else {
 return (new XMLSerializer()).serializeToString(oXML);
 }
 }
function Crop()
{
    $('#BaseCanvas').click(function (){removeSelection();});
     $('#BaseCanvas').imgAreaSelect({
        handles: true,
        onSelectEnd: SelectCrop,
        onSelectChange:function (img, selection) {
        if(selection.width == 0)
            removeSelection();
    }
         
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