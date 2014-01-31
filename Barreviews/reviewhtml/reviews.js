function SaveReviewComments()
{
    var data = {'rating': $("#rating").val(),'description': encodeURIComponent($("#curdescription").val()),'favsnack1': $('#snack1').val(),'favsnack2':$('#snack2').val(),'reviewid':$('#reviewid').val()};
    console.log(data);
     $.ajax({
               type: "GET",
               url: "/api/b/updatecomment",
               data:data,
               success: function(response){
                    var klon = $("#reviewItem" );
                    var container = $('#revContainer');
                    var oClone = klon.clone();
                    $(oClone).find('#creatorname').html($("#curcreatorname").html());
                    $(oClone).find('#creatoravatar').attr('src',$('#curcreatoravatar').attr('src'));
                    $(oClone).find('#creatoravatar').attr('src',$("#curcreatorname").attr('src'));
                   $(oClone).find('#creatordescription').html(decodeURIComponent($("#curdescription").val()));
                   if($("#rating").val() == 1)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_1_0.png');
                   if($("#rating").val() == 1.5)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_1_5.png');
                   if($("#rating").val() == 2)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_2_0.png');
                   if($("#rating").val() == 2.5)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_2_5.png');
                   if($("#rating").val() == 3)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_3_0.png');
                   if($("#rating").val() == 3.5)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_3_5.png');
                   if($("#rating").val() == 4)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_4_0.png');
                   if($("#rating").val() == 4.5)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_4_5.png');
                   if($("#rating").val() == 5)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_5_0.png');
                    //$(container).prepend('<div class = "separator"></div>');
                    $(container).prepend(oClone);
                    $(oClone).show();


               }
    });
}

function UpdateReviewComments()
{
	$('#curEditContainer').find('#spinner').show();
    var data = {'rating': $('#curEditContainer').find("#rating").val(),'review': $('#curEditContainer').find("#curdescription").val(),'reviewid':$('#curEditContainer').find('#rid').val()};
    console.log(data);
     $.ajax({
               type: "GET",
               url: "/api/b/updateusercomment",
               data:data,
               success: function(response){
               		if ($('#curEditContainer').find('#descreview').val() == "1") {
               			location.reload();
               		} else {
			   			$('#curEditContainer').find('#spinnerMg').html("Updated your Review...").delay(5000).hide();
			   			$('#curEditContainer').find('#spinner').hide();
			   		}
               }
    });
}

function ListLatestReviews()
{
    $.ajax({
               type: "GET",
               url: "/api/b/list?limit=10&offset=0",
               //url: "/reviews/scenes/listscenes?limit=2&offset=0",
	       dataType:"xml",
               success: function(response){
                    //theXmlDoc = $.parseXML(response);
                    var theRow = $(response).find('review').get();
                    $(theRow).each(function(i) 
                    {
                        i++;
                        var review_name = $(this).children('name').text();
                        var imgUrl = $(this).children('icon').text();
                        var url    =  $(this).children('url').text();
                        $('#gallery-list-reviews').find('#item_'+i).find('img').attr('src',imgUrl);
                        $('#gallery-list-reviews').find('#item_'+i).find('h6').html(review_name);
                        
                        $('#gallery-list-reviews').find('#item_'+i).click(function()
                        {
                            window.location =  url;
                        });                                                      
                    });
               }
    });
}
function ListLatestOh()
{
    $.ajax({
               type: "GET",
               url: "/api/oh/list?limit=10&offset=0",
               //url: "/reviews/scenes/listscenes?limit=2&offset=0",
               success: function(response){
                    theXmlDoc = $.parseXML(response);
                    var theRow = $(theXmlDoc).find('meme').get();
                   
                    $(theRow).each(function(i) 
                    {
                        i++;
                        var imgUrl = $(this).find('icon').text();
                        var url    =  $(this).find('url').text();
                        $('#gallery-list-memes').find('#meme_'+i).find('img').attr('src',imgUrl);
                        //$('#gallery-list-reviews').find('#item_'+i).find('h6').html(review_name);
                        
                        $('#gallery-list-memes').find('#meme_'+i).click(function()
                        {
                            window.location =  url;
                        });                                                      
                    });
               }
    });
}

function editBar(ele)
{
    var bid = $(ele).attr('value');
    window.location =  "/b/edit/"+bid;
    return false;
}
function toggleEditOption (ele)
{
    var parent = $(ele).parent().parent();
    $(parent).find('#bEditWrapper').toggle();
}
function InitBox()
{
    
}
var fromBar = false;
function AddOverheard()
{
	$('#fullScreenLoader').show();
	window.scrollTo(0, 0);
    fromBar = true;
    
    $.ajax({
               type: "GET",
               url: "/oh/brecord",
               success: function(response){
                        $('body').append(response);
                        $("#oh").dialog({
                        height: 'auto',
                        width: 'auto',
                        open: function( event, ui ) {
                        	$('#fullScreenLoader').hide();
                        },
                        close:closedialog,
                        minWidth: 1080,
                        modal:true,
                        position: 'center',
                        resizable: false,
                        draggable:false,
                        dialogClass:"customDialog"
                   });

        }
    });
    
}
function closedialog() {
 $("#oh").remove();
};
function FromBar(id)
{
    closedialog();
    $('#OhAtContainer').empty();
    $.ajax({
            type: 'GET',
            url: '/api/b/overheards?bid='+$('#bid').val(),
            success: getBarOverHeards,
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                        //TODO
            }
    }); 
}

function showBarOh(a_ele)
{
	var bid = $(a_ele).attr('value');
	/* Get OverHeards */
	var modal = $('#ohModalTpl').clone().attr('id','modal_'+bid);
	$(modal).dialog({
		height: 'auto',
		width: 'auto',
		open: function( event, ui ) {
			var loader = $('#fullScreenLoader');
			$(modal).append(loader);
			$(loader).show();
		},
		close: function( event, ui ) {
			$(modal).remove();
		},
		modal:true,
		position: 'center',
		resizable: false,
		draggable:false,
		dialogClass:"customDialogOh"
   });
   
   $('.customDialogOh').scroll(function()
   {
    	if($('.customDialogOh').scrollTop() > 0)
    	{
    		$('.customDialogOh').find('#scrolltoTop').show();
    	}
    	else
    	{
    		$('.customDialogOh').find('#scrolltoTop').hide();
    	}
   });
   
    $.ajax({
            type: 'GET',
            url: '/api/b/overheards?bid='+bid,
            success: getBarOhModal,
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                        //TODO
            }
    });
}

function getBarOhModal (data)
{
	$('.fullScreenLoaderModal').hide();
	theXmlDoc = $.parseXML(data);
    var theRow = $(theXmlDoc).find('meme').get();
    var len    = $(theXmlDoc).find('meme').length;
    if (len == 0) {
    	var noContent = $('#ohNoContent').clone();
    	$('.oc').append(noContent);
    	$(noContent).show();
    }
    $(theRow).each(function(i)
    {
    	i++;
    	var icon = $(this).find("icon").text();
    	var url  = $(this).find("url").text();
    	var arr  = url.split("/");
    	var mid  = arr.pop();
    	var ele  = $('#ohThumbs').clone().attr('id','bOhIndv_'+i);
    	$(ele).find('img').attr('src',icon);
    	$(ele).find('.shareFB a').click(function()
    	{
    		shareOhOnFaceBook(mid,'private');
    	});
    	$(ele).find('.shareTwitter a').click(function()
    	{
    		shareOhOnTwitter(mid);
    	});
    	$(ele).find('.shareGoogle a').click(function()
    	{
    		shareOhOnGoogle(mid);
    	});
    	$('.oc').append(ele);
    	$(ele).show();
    	if (i== len)
    	{
    		
    	}
    });
}

function scrollOhToTop (a_ele)
{
	$('.customDialogOh').scrollTop(0);
}
