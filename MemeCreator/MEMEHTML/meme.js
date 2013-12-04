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
function UploadSkeleton()
{
    var options = {success:       SkeletonUploaded};
    $('#uploadNewForm').ajaxForm(options);
    $('#uploadNewForm').submit();
}
function SkeletonUploaded(data)
{
    $('#uploadNewForm').remove();
    var api = $(".itemsCore").empty();
    GetThumbnails();
    GetUploadURL();
}
function UploadUrlSkeleton(data)
{
     var html = '<form action="'+data+'" id="uploadNewForm" method="POST" enctype="multipart/form-data"><input type="file" name="content" class = "myFile" id="myFile" style="display:none;"/><>      <input type="hidden" id="tags" value="smashed,jaggesh" name = "tags" /> </form>';
    $('body').append(html);     
}
function GetUploadURL()
{
    $.ajax({
        url: "/api/oh/skel-preupload",
        type: 'GET',
        crossDomain: true,
        
    }).done(function ( data ) {
        $("#uploadNewForm").attr('action',data);
        UploadUrlSkeleton(data);        
    });
}
function ChangeBackground()
{   
    $("#myFile").click();      
    $('#myFile').change(function(input)
    {        
        UploadSkeleton();
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

function AddCaption()
{
    reset();
    i++;
    var top = 10;
    if(i== 1)
        top = 10;
    else if(i == 2)
        top = 400;
        
        
    $("#BaseCanvas").append("<div class='demo"+i+"' style='width:200px;height:40px;x:0px;y:0px;position:absolute;left:200px;top:"+top+"px;background-color:transparent;'><textarea  id='myText"+i+"' class='displayBlock' style='width:100%;height:100%;x:0px;y:0px;position:absolute;top:0; border-color:transparent;background-color:transparent;overflow:hidden;'>Add caption here</textarea></div>");  
    
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
            curDemoBox.css("top",event.pageY - 280 - $(cuTextBox).height()/2);
            curDemoBox.css("left",event.pageX - 100 - $(cuTextBox).width()/2);
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
    GetUploadURL();
      // initialize scrollable
      $('#color1').colorPicker();
      //$(".scrollable").scrollable();
      $("#BaseCanvas").droppable({
      drop: function( event, ui ) {
            curImage =  $("#backImage");
            curImage.addClass('imagehide');
            var iconsrc = ui.draggable.find("img").context.src;
            var src = iconsrc.replace("icon", "download");
            var value = iconsrc.split("/").pop();

            $("#backImage").attr('src', src);
          
            $("#backImage").attr('value', value);
          
            $('#saveButton').removeClass("disabled");   
            $('#saveButton').addClass("enabled");   
            $("#saveButton").removeAttr("disabled");
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
        url: "/api/oh/skel-list",
        type: 'GET',
        crossDomain: true,
    }).done(function ( data ) {
               theXmlDoc = $.parseXML(data);
			   var theRow = $(theXmlDoc).find('url').get();
			   $(theRow).each(function(i) 
				{
				    var test = '<div class="scrollableDiv col-lg-5" ><img class="widthCLass" id="image_'+i+'"  src="'+$(this).text()+'"/></div>';                   
				    $('.itemsCore').append(test); 
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
    console.log(cuTextBox);
    curFontSize = val;
    cuTextBox.css("font-size",val+"px");
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
    
    var oImages = document.createElement('imagebase')
    oImages.setAttribute("id",curImage.val());
    oImages.setAttribute("width",curImage.width());
    oImages.setAttribute("height",curImage.height());
    oObjetcs.appendChild(oImages);
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
   
    xmlDocument.documentElement.appendChild(oObjetcs);
    
    /* Spinners */
    $('#memeSpinner').fadeIn();
    
    $.ajax({
      type: "POST",
      crossDomain: true,
      url: '/api/oh/save',
        data : {
            method : "Save",
            data : XMLToString(xmlDocument)
        },

    }).done(function ( datanew ) {
        window.location = '/oh/'+datanew;
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
function UploadSuccessData(id)
{
    $.ajax({
        url: "/meme/store/facebookupload/"+id,
        type: 'GET',
        crossDomain: true,
        
    }).done(function ( data ) {
        ShareToFacebook(data,id);        
    });
}
var socialUrl = "";
function ShareToFacebook(data,id)
{
	var splitres = id.split(":");
	var postid = splitres[1];
	socialUrl = "https://www.facebook.com/photo.php?fbid="+postid;
	//alert(socialUrl);
	console.log($("#facebookshare"));
	$("#facebookshare").click();
	
}
var popupwindow;
function UploadToFacebook(imgURL)
{
	popupwindow = custompopup('', {
				width: 480,
				height: 300
			});
	FB.api('/me/photos', 'post', {
	access_token: oStrAccessToken,
		message:'photo description',
		url:'http://smashed.thejasvi.in'+imgURL        
	}, function(response){

		if (!response || response.error) {
			//alert('Error occured');
			UploadSuccessData($("#currentid").val() + ":" + "theju");
		} else {
			UploadSuccessData($("#currentid").val() + ":" + response.id);
			//alert('Post ID: ' + response.id);
		}

	});
}
function custompopup(url, params) {
		var left = Math.round(screen.width/2 - params.width/2),
			top = 0;
		if (screen.height > params.height) {
			top = Math.round(screen.height/3 - params.height/2);
		}

		var win = window.open(url, 'sl_' + this.service, 'left=' + left + ',top=' + top + ',' +
			'width=' + params.width + ',height=' + params.height + ',personalbar=0,toolbar=0,scrollbars=1,resizable=1');
		if (win) {
			win.focus();
		} else {
			location.href = url;
		}
		return win;
	}
