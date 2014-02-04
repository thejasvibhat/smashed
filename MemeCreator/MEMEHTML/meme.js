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
var privateMode = false;
var init = false;

var tabindex = 1;
function TabsInit()
{
    if($('#tabvalue').val() == 'gallery')
        tabindex = 0;
    $('#tabs,#gallery').tabs({
        active: tabindex,
        activate: function(event, ui){
          var curIndex = ui.newTab.index();
          if(curIndex != tabindex)
          {
            if(curIndex == 0)
                window.location = '/oh';
            else
                window.location = '/oh/page/mine/1';
          }
        }
    });
}

function Init()
{
    $( "#accordion" ).accordion({
      heightStyle: "content",
         autoHeight: true,
        collpsible: true, 
    });
}
function UploadSkeleton()
{
    
    var options = {success:SkeletonUploaded};
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
function PrivateMode()
{
    privateMode = !privateMode;
    if(privateMode)
    {
        $("#pmode").val("ON");
        $("#pmode").removeClass("btn-warning");
        $("#pmode").addClass("btn-success");     
        $("#pmodeOverall").val("ON");
        $("#pmodeOverall").removeClass("btn-success");
        $("#pmodeOverall").addClass("btn-warning"); 
        $("#pmodeOverall").attr("title","Click to enable Public mode");     
        $("#privatemode").val("private");
        $("#save").removeClass("btn-success");
        $("#save").addClass("btn-warning");
        $('#pmode').attr('checked',false);

    }
    else
    {
        $("#pmode").val("OFF");
        $("#pmode").removeClass("btn-success");        
        $("#pmode").addClass("btn-warning");
        $("#pmodeOverall").val("OFF");
        $("#pmodeOverall").removeClass("btn-warning");            
        $("#pmodeOverall").addClass("btn-success");        
        $("#pmodeOverall").attr("title","Click to enable Private mode");
        $("#privatemode").val("public");
        $("#save").removeClass("btn-warning");            
        $("#save").addClass("btn-success");
        $('#pmode').attr('checked',true);
        
    }
    
}
function SkeletonUploaded(data)
{
    $('#uploadNewForm').remove();
    var api = $(".itemsCoreMine").empty();    
    GetUploadURL();
    setTimeout(function () {
            GetMyUploads();
            if(privateMode)
            {
                GetMyUploads();
            }
            else
            {
                GetThumbnails();
            }
        }, 100);
    
}
function UploadUrlSkeleton(data)
{
     var html = '<form action="'+data+'" id="uploadNewForm" method="POST" enctype="multipart/form-data"><input type="file" name="content" class = "myFile" id="myFile" style="display:none;"/> <input type="hidden" id="tags" value="smashed,jaggesh" name = "tags" /><input type="hidden" name="pmode" id="privatemode" value="public" ></p></form>';
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
function clear()
{
    iTextCnt = 0;
	m_arrGrids.splice(0,m_arrGrids.length);
	m_arrTextBoxes.splice(0,m_arrTextBoxes.length);
	m_arrDemoBoxes.splice(0,m_arrDemoBoxes.length);
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
    var base = $("#BaseCanvas");
    if(ohtype == "Conversation")
        base = $("#ConversationCanvas");
    $(base).append("<div class='demo"+iTextCnt+"' style='line-height:30px;width:500px;min-height:100px;x:0px;y:0px;position:absolute;top:"+top+"px;left:15px;margin-left:0;background-color:transparent;cursor:move;'><textarea placeholder = 'Add caption here'  id='myText"+iTextCnt+"' class='displayBlock' style='padding-left:42px;text-align:center;resize:none;width:100%;height:100%;x:0px;y:0px;position:absolute;top:0; border-color:transparent;background-color:transparent;overflow:hidden;border:none;cursor:move;text-shadow: 2px 2px #000;'></textarea></div>");  
    
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
  
   $(base).mousemove(function moveall(event){
        
        if(isDragging)
        {
            var localCoordinates = $(base).globalToLocal(
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
function HandleSkelClick(imageSkel,url,id)
{
    $(imageSkel ).click(function() {
                curImage =  $("#backImage");
                curImage.addClass('imagehide');
                var iconsrc = this.src;
                var src = iconsrc.replace("icon", "download");
                var value = iconsrc.split("/").pop();
                if(ohtype == "Conversation")
                {
                        $.each(m_arrGrids,function(index,grid){
                            var curImg = $(grid).find("#backImageCon");
                            if(curImg.val() == 'default')
                            {
                                curImg.attr('src', url);
                                curImg.attr('sid', id);
                                curImg.val('actual');
                                $.each(m_arrGrids,function(griindex,gridtemp){
                                    var newcurImg = $(gridtemp).find("#backImageCon");
                                    if(newcurImg.val() == "undefined" || (newcurImg.val() != "actual"))
                                    {
                                        ReadyForSkel(gridtemp);
                                        return false;
                                    }
                                });
                                $(grid).mouseenter(function(){
                                    if(curImg.val() == 'actual')
                                    {
                                        var oPd = $("#removePanel").clone();
                                        
                                        $(grid).append(oPd);
                                        $(oPd).show();
                                    
                                   
                                        $(oPd).click(function(event){
                                        
                                            $(curImg).val('default');
                                            curImg.attr('src', '/static/img/drophere.png');
                                            $( grid ).find( "#removePanel" ).remove();
                                        });
                                    }
                               
                                });
                                 $(grid).mouseleave(function() {
                                    $( grid ).find( "#removePanel" ).remove();
                                
                                });
                                return false;
                            }
                            
                        });
                }
                else
                {
                    $("#backImage").attr('src', url);        
                }
		
                $("#BaseCanvas").addClass('load');  
                $("#backImage").attr('value', id);
                $('#saveButton').removeClass("disabled");   
                $('#saveButton').addClass("enabled");   
                $("#saveButton").removeAttr("disabled");
	    });
	    $(imageSkel ).load(function () {                
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
}
function GetMyUploads(tags)
{
    $('.itemsCoreMine').empty();
    var lUrl = "/api/oh/skel-list?limit=1000";
    var data = {};
    data.mode="mine";
    if(tags)
    {
        data.tag=tags;
    }
    $.ajax({
        url: lUrl,
        type: 'GET',
        data: data,
        crossDomain: true,
    }).done(function ( data ) {
	$(data).find("skel").each (function() {
	    var id = $(this).find("id").text();
	    var thumburl = $(this).find("thumburl").text();
	    var url = $(this).find("url").text();

	    html_id = id.replace (/[^\w\s]/gi, '');
	    var test = '<div class="scrollableDiv col-lg-5" ><img class="widthCLass tilt" id="image_'+html_id+'" src="'+thumburl+'"/></div>';
	    $('.itemsCoreMine').append(test);
        HandleSkelClick($( "#image_"+html_id ),url,id);
	    

	});
    });
    $( "#accordion" ).accordion({
      heightStyle: "content",
         autoHeight: true,
        collpsible: true, 
    });
    $("#accordion").accordion("refresh");
    return false;
}
function GetThumbnails(tags)
{
   /* if(init)
    {
        var active = $( "#accordion" ).accordion( "option", "active" );
       // if(active == 1)
        {
            GetMyUploads(tags);  
           // return;
        }
        
    }*/
    GetMyUploads(tags);  
    init = true;
    $('.itemsCore').empty();
    var lUrl = "/api/oh/skel-list?limit=1000";
    var data = {};
    data.mode="public";
    if(tags)
    {
        data.tag=tags;
    }
    $.ajax({
        url: lUrl,
        type: 'GET',
        data: data,
        crossDomain: true,
    }).done(function ( data ) {
	$(data).find("skel").each (function() {
	    var id = $(this).find("id").text();
	    var thumburl = $(this).find("thumburl").text();
	    var url = $(this).find("url").text();

	    html_id = id.replace (/[^\w\s]/gi, '');
	    var test = '<div class="scrollableDiv col-lg-5" ><img class="widthCLass tilt" id="image_'+html_id+'" src="'+thumburl+'"/></div>';
	    $('.itemsCore').append(test);

	    HandleSkelClick($( "#image_"+html_id ),url,id);

	});
    });
    $( "#accordion" ).accordion({
      heightStyle: "content",
         autoHeight: true,
        collpsible: true, 
    });
    $("#accordion").accordion("refresh");
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
	$('#parentContainer').scrollTop(0);
    var base = $("#BaseCanvas");
    
    removeSelection();
    var xmlDocument = $.parseXML("<root/>");
    var oObjetcs = document.createElement('objects');
    if(ohtype == "Conversation")
    {
        base = $("#ConversationCanvas");
        oObjetcs.setAttribute("type","conversation");
        var rows = $("#rows").val();
        var columns = $("#columns").val();
        oObjetcs.setAttribute("rows",rows);
        oObjetcs.setAttribute("columns",columns);
    }
    oObjetcs.setAttribute("x",curSelectionX);
    oObjetcs.setAttribute("y",curSelectionY);
    oObjetcs.setAttribute("width",$(base).width());
    oObjetcs.setAttribute("height",$(base).height());
    if(ohtype == "Conversation")
    {
        for(i=0;i<m_arrGrids.length;i++)
        {
            curImage = $(m_arrGrids[i]).find('#backImageCon');
            var oImages = document.createElement('imagebase')
            oImages.setAttribute("id",curImage.attr('sid'));
            oImages.setAttribute("width",curImage.width());
            oImages.setAttribute("height",curImage.height());
            oObjetcs.appendChild(oImages);
        }
    }
    else
    {
        var oImages = document.createElement('imagebase')
        oImages.setAttribute("id",curImage.val());
        oImages.setAttribute("width",curImage.width());
        oImages.setAttribute("height",curImage.height());
        oObjetcs.appendChild(oImages);
    }
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
        oProperty.setAttribute("left",m_arrDemoBoxes[i].css("left").split("p")[0] - $(base).position().left+42);
        oProperty.setAttribute("top",m_arrDemoBoxes[i].css("top").split("p")[0] - $(base).position().top);
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
    var mode = 'gallery';
    if(privateMode)
        mode = 'private';
    var urloh =  '/api/oh/save?mode='+mode;
    if (typeof fromBar === 'undefined') {
    // variable is undefined
    }
    else
    {
        if(fromBar == true)
            urloh = '/api/oh/save?bid='+$("#bid").val()+'&mode='+mode;
    }
    $.ajax({
      type: "POST",
      crossDomain: true,
      url: urloh,
        data : {
            method : "Save",
            data : XMLToString(xmlDocument)
        },

    }).done(function ( datanew ) {
        if (typeof fromBar === 'undefined')
        {
            window.location = '/oh/'+datanew;
        }
        else
        {
            if(fromBar)
            {
                FromBar(datanew);
            }
        }
            
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
function UpdateStepperUpRows()
{
    var targInput = $("#rows");
    var value = targInput.val();
    value++;
    var min = 1;
    var max = 4;
    if ((value > min)&&(value <= max))
        targInput.val(value);
    GridChange();
}
function UpdateStepperDownRows()
{
    var targInput = $("#rows");
    var value = targInput.val();
    value--;
    var min = 1;
    var max = 4;
    if ((value < max)&&(value >= min))
        targInput.val(value);
    GridChange();
}
function UpdateStepperUpColumns()
{
    var targInput = $("#columns");
    var value = targInput.val();
    value++;
    var min = 1;
    var max = 2;
    if ((value > min)&&(value <= max))
        targInput.val(value);
    GridChange();
}
function UpdateStepperDownColumns()
{
    var targInput = $("#columns");
    var value = targInput.val();
    value--;
    var min = 1;
    var max = 2;
    if ((value < max)&&(value >= min))
        targInput.val(value);
    GridChange();
}
var canCon;
var sepCon;
var m_arrGrids = [];
var currentGrid;
var ohtype;
var backImageCon;
function GridChange()
{
	
    clear();
    if(!canCon)
    {
        canCon = $("#canCon");
        sepCon = $("#sepcon").clone();
    }
    $('#ConversationCanvas').empty()
   // $('#ConversationCanvas').append(canCon);
  //  $('#ConversationCanvas').append(sepCon);
    
    var rows = $("#rows").val();
    var columns = $("#columns").val();
    var cheight = 500/rows;
    var cwidth = 500/columns;
    if (parseInt(rows) > 2) {
    	cheight = 250;
    	$('#ConversationCanvas').css('height',cheight*parseInt(rows));
    } else {
    	$('#ConversationCanvas').css('height',500);
    }
   
    //alert(cheight);
    $(canCon).height(cheight);
    $(canCon).width(cwidth);
    for(i=0 ; i < rows ; i++)
    {
        var sepCon = $(sepCon).clone();
        var cloneCan = $(canCon).clone();
        cloneCan.attr("id","cloneRow"+i);
        $("#ConversationCanvas").append(cloneCan);
        cloneCan.css('border-bottom', "solid 1px white");
        if(columns > 1)
        {
            cloneCan.css('border-right', "solid 1px white");
            cloneCan.css('display', "inline-block");
        }
        m_arrGrids.push(cloneCan);
        for (j=1 ; j < columns ; j++)
        {
            var cloneCanCol = $(canCon).clone();
            cloneCanCol.attr("id",cloneCan.attr('id')+j);
            $("#ConversationCanvas").append(cloneCanCol); 
            cloneCanCol.css('border-right', "solid 1px white");
            cloneCanCol.css('border-bottom', "solid 1px white");
            cloneCanCol.css('display', "inline-block");
            m_arrGrids.push(cloneCanCol);
        }
        
    }
    ConGridClicked(m_arrGrids[0])
}
function ReadyForSkel(grid)
{
        var imgsrc = $(backImageCon).clone();
        //$(imgsrc).width($(currentGrid).width());
        //$(imgsrc).height($(currentGrid).height());
        imgsrc.val('default');
        imgsrc.attr('src', '/static/img/drophere.png');
        $(imgsrc).show();
        $(grid).append(imgsrc);
        currentGrid = grid;
}
function ConGridClicked(grid)
{
    if(!backImageCon) {
        backImageCon = $("#backImageCon").clone();
        $('#backImageCon').attr('id','old');
        $(backImageCon).attr('id','backImageCon');
    }
    $('#old').remove();	
    $.each(m_arrGrids,function(index,gridtemp){
        var curImg = $(gridtemp).find("#backImageCon");
        if(curImg.val() != 'actual')
            curImg.remove();
    });
    currentGrid = grid;
    if($(currentGrid).children().length == 0)
    {
        var imgsrc = $(backImageCon).clone();
        //$(imgsrc).width($(currentGrid).width());
        //$(imgsrc).height($(currentGrid).height());
        imgsrc.val('default');
        $(imgsrc).show();
        $(currentGrid).append(imgsrc);
    }
   
}
function UpdateType(val)
{
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
function OnImageLoadConGrid(curImageView)
{
    if(ohtype == "Conversation"){
        curImage = $(curImageView);
        if(curImage.width() == 0)
            return;
        
        var ht = 'max-height:'+$(currentGrid).height()+'px;max-width:'+$(currentGrid).width()+'px';
            curImage.attr('style',ht);
            var margin = 'margin:' +($(currentGrid).height() - curImage.height())/2+'px 0px 0px '+($(currentGrid).width() - curImage.width())/2+'px;'+'max-height:'+$(currentGrid).height()+'px;max-width:'+$(currentGrid).width()+'px;position:absolute;';
            curImage.attr('style',margin);
        /*
        if((curImage.height()) > (curImage.width()))
        {     
            var ht = 'max-height:'+$(currentGrid).height()+'px;max-width:'+$(currentGrid).width()+'px';                            
            curImage.attr('style',ht);
            var margin = 'margin: 0px 0px 0px '+($(currentGrid).width() - curImage.width())/2+'px;'+'max-height:'+$(currentGrid).height()+'px;max-width:'+$(currentGrid).width()+'px;position:absolute;';                            
            curImage.attr('style',margin);
            
        }
        else
        {
            var wt = 'max-height:'+$(currentGrid).height()+'px;max-width:'+$(currentGrid).width()+'px';                                               
            curImage.attr('style',wt);
            var margin = 'margin: '+($(currentGrid).height() - curImage.height())/2+'px 0px 0px 0px;'+'max-height:'+$(currentGrid).height()+'px;max-width:'+$(currentGrid).width()+'px;position:absolute;';                            
            curImage.attr('style',margin);
        }*/
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
        $(oClone).find('#ticktext').html($(this).find('ticktext').text());
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
           $(oClone).find('#ticktext').html($(this).find('ticktext').text());
			$(container).prepend('<div class = "separator"></div>');
			$(container).prepend(oClone);
			$(oClone).show();
	   }
    });
}

