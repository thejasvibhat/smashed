var isDragging = false;
var iTextCnt = 0;
var cuTextBox;
var curDemoBox;
var curColor = '#fff';
var curFontSize = 20;
var curfontFamily = "Impact";
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
function SaveSkel()
{
    $("#modalView").addClass('overlayout');
    $("#modalView").removeClass('popup');
    $("#tags").val($("#tags_2").val());
    UploadSkeleton();
}

function CancelSaveSkel ()
{
	$("#modalView").addClass('overlayout');
    $("#modalView").removeClass('popup');
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
     var html = '<form action="'+data+'" id="uploadNewForm" method="POST" enctype="multipart/form-data"><input type="file" name="content" class = "myFile" id="myFile" style="display:none;"/> <input type="hidden" id="tags" value="smashed,jaggesh" name = "tags" /> </form>';
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
         var file = input.target.files[0];
        var reader = new FileReader();

        reader.readAsDataURL(file);
        reader.onloadend = function(e) {
            $("#thumb1").attr('src', e.target.result);  
            $("#modalView").removeClass('overlayout');
            $("#modalView").addClass('popup');
        }

      //  UploadSkeleton();
    }); 
}
function reset()
{
    curColor = '#fff';
    curFontSize = 30;
    curfontFamily = "Impact";
    curfontWeight = "Normal";
    curfontStyle = "Normal";
}

function AddCaption()
{
    reset();
    iTextCnt++;
    var top = 10;
    if(iTextCnt== 1)
        top = 10;
    else if(iTextCnt == 2)
        top = 400;
        
        
    $("#BaseCanvas").append("<div class='demo"+iTextCnt+"' style='line-height:30px;width:550px;min-height:100px;x:0px;y:0px;position:absolute;top:"+top+"px;left:15px;background-color:transparent;cursor:move;'><textarea placeholder = 'Add caption here'  id='myText"+iTextCnt+"' class='displayBlock' style='text-align:center;resize:none;width:100%;height:100%;x:0px;y:0px;position:absolute;top:0; border-color:transparent;background-color:transparent;overflow:hidden;border:none;cursor:move;text-shadow: 2px 2px #000;'></textarea></div>");  
    
    cuTextBox = $('#myText'+iTextCnt+'');     
    m_arrTextBoxes.push(cuTextBox);
    ColorChanged(curColor);
    curFontSize = $('#fontSize').val();
    FontSizeChange(curFontSize);
    UpdateFamily(curfontFamily);
    UpdateFontweight(curfontWeight);
    UpdateFontStyle(curfontStyle);
    var textBox = $('#myText'+iTextCnt+'');
    var demoBox = $('.demo'+iTextCnt+'');
    m_arrDemoBoxes.push(demoBox);
    curDemoBox = demoBox;
    textBox.focus();
    demoBox.addClass("backgroundTransparent");
    textBox.mousedown(function down(ev){cuTextBox = textBox;isDragging = true;
                                        demoBox.removeClass("backgroundTransparent");});
  
   $("#BaseCanvas").mousemove(function moveall(event){
        
        if(isDragging)
        {
            var localCoordinates = $("#BaseCanvas").globalToLocal(
						event.pageX,
						event.pageY
					);
            curDemoBox.css("top",localCoordinates.y - $(cuTextBox).height()/2);
            curDemoBox.css("left",localCoordinates.x - $(cuTextBox).width()/2);
        }
   });
    demoBox.mouseup(function up(ev){curDemoBox = demoBox;isDragging = false;});
    demoBox.mousedown(function updown(ev){curDemoBox = demoBox;});
  
   } 

function RemoveCaption()
{
    var index = m_arrDemoBoxes.indexOf(curDemoBox);
    if (index > -1) {
        m_arrDemoBoxes.splice(index, 1);
        m_arrTextBoxes.splice(index, 1);
    }

    curDemoBox.remove();
}
function Apply()
{
    var fontsize = $("#fontsize").val() + 'px';
    cuTextBox.css("font-size",fontsize);
}
/*
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
    $('#tags_2').tagsInput({
				width: 'auto',
				onChange: function(elem, elem_tags)
				{
					var languages = ['php','ruby','javascript'];
					$('.tag', elem_tags).each(function()
					{
						if($(this).text().search(new RegExp('\\b(' + languages.join('|') + ')\\b')) >= 0)
							$(this).css('background-color', 'yellow');
					});
				}
			});
});
*/
function SelectCrop(div,selection)
{
    curSelectionX = selection.x1/450;
    curSelectionY = selection.y1/450;
    curSelectionWidth = selection.x2/450;
    curSelectionHeight = selection.y2/450;
}
function TagPressed(e){
    if (!e) e = window.event;
    var keyCode = e.keyCode || e.which;
    if (keyCode == '13'){
      GetThumbnails($("#search").val());
      return false;
    }
  }
function GetThumbnails(tags)
{
    $('.itemsCore').empty();
    var lUrl = "/api/oh/skel-list";
    if(tags)
        lUrl = "/api/oh/skel-list?tag="+tags;
    $.ajax({
        url: lUrl,
        type: 'GET',
        crossDomain: true,
    }).done(function ( data ) {
	$(data).find("skel").each (function() {
	    var id = $(this).find("id").text();
	    var thumburl = $(this).find("thumburl").text();
	    var url = $(this).find("url").text();

	    html_id = id.replace (/[^\w\s]/gi, '');
	    var test = '<div class="scrollableDiv col-lg-5" ><img class="widthCLass tilt" id="image_'+html_id+'" src="'+thumburl+'"/></div>';
	    $('.itemsCore').append(test);

	    $( "#image_"+html_id ).click(function() {
                curImage =  $("#backImage");
                curImage.addClass('imagehide');
                var iconsrc = this.src;
                var src = iconsrc.replace("icon", "download");
                var value = iconsrc.split("/").pop();
		$("#backImage").attr('src', url);
                $("#BaseCanvas").addClass('load');  
                $("#backImage").attr('value', id);
                $('#saveButton').removeClass("disabled");   
                $('#saveButton').addClass("enabled");   
                $("#saveButton").removeAttr("disabled");
	    });
	    $( "#image_"+html_id ).load(function () {                
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
	if (val != "Impact") {
		$('#fontStyle').attr('disabled',false);
		$('#fontWeight').attr('disabled',false);	
	} else {
		$('#fontStyle').attr('disabled',true);
		$('#fontWeight').attr('disabled',true);	
	}
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
    var oObjetcs = document.createElement('objects');
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
    var targInput = $("#fontSize");
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
    var targInput = $("#fontSize");
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
    $("#BaseCanvas").removeClass('load');
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

// I translate the coordiantes from a global context to
// a local context.
$.globalToLocal = function( context, globalX, globalY ){
    // Get the position of the context element.
    var position = context.offset();

    // Return the X/Y in the local context.
    return({
        x: Math.floor( globalX - position.left ),
        y: Math.floor( globalY - position.top )
    });
};


// I translate the coordinates from a local context to
// a global context.
jQuery.localToGlobal = function( context, localX, localY ){
    // Get the position of the context element.
    var position = context.offset();

    // Return the X/Y in the local context.
    return({
        x: Math.floor( localX + position.left ),
        y: Math.floor( localY + position.top )
    });
};


// -------------------------------------------------- //
// -------------------------------------------------- //


// I am the FN version of the global to local function.
$.fn.globalToLocal = function( globalX, globalY ){
    return(
        $.globalToLocal(
            this.first(),
            globalX,
            globalY
        )
    );
};


// I am the FN version of the local to global function.
$.fn.localToGlobal = function( localX, localY ){
    return(
        $.localToGlobal(
            this.first(),
            localX,
            localY
        )
    );
};


// -------------------------------------------------- //
// -------------------------------------------------- //

function GetTickerInit()
{
	$.ajax({
        url: "/api/oh/list?offset=0&limit=10",
        type: 'GET',
        crossDomain: true,
        
    }).done(function ( data ) {
       // alert(data);
	   theXmlDoc = $.parseXML(data);
	   var theRow = $(theXmlDoc).find('meme').get();
	  $(theRow).each(function(i) 
	  {
	   	var klon = $("#tickItem" );
	   	var container = $('#tickerContainer');
	   	var oClone = klon.clone();
	   	$(oClone).find('#ticks').attr('href',$(this).find('url').text());
       	$(oClone).find('#creatorname').html($(this).find('creatorname').text());
	   	$(oClone).find('#creatoravatar').attr('src',$(this).find('creatoravatar').text());
	   	$(container).prepend('<div class = "separator"></div>');
	   	$(container).prepend(oClone);
	   	$(oClone).show();
	  });
    });
    
}

function GetTickerLatest()
{
	$.ajax({
        url: "/api/oh/list?offset=0&limit=1",
        type: 'GET',
        crossDomain: true,
        
    }).done(function ( data ) {
       // alert(data);
	   theXmlDoc = $.parseXML(data);
	   var theRow = $(theXmlDoc).find('ts').text();
	   if(m_strCurTimeStamp == "")
			m_strCurTimeStamp = theRow;
	   if(theRow != m_strCurTimeStamp)
	   {
			m_strCurTimeStamp = theRow;
			var klon = $("#tickItem" );
			var container = $('#tickerContainer');
			var oClone = klon.clone();
			$(oClone).find('#ticks').attr('href',$(theXmlDoc).find('url').text());
			$(oClone).find('#creatorname').html($(theXmlDoc).find('creatorname').text());
			$(oClone).find('#creatoravatar').attr('src',$(theXmlDoc).find('creatoravatar').text());
			$(container).prepend('<div class = "separator"></div>');
			$(container).prepend(oClone);
			$(oClone).show();
	   }
    });
}

