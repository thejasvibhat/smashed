function SaveReviewComments()
{
    var data = {'rating': $("#rating").val(),'description': $("#curdescription").val(),'favsnack1': $('#snack1').val(),'favsnack2':$('#snack2').val(),'reviewid':$('#reviewid').val()};
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
                   $(oClone).find('#creatordescription').html($("#curdescription").val());
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
			   		$('#curEditContainer').find('#spinnerMg').html("Updated your Review...").delay(5000).hide();
			   		$('#curEditContainer').find('#spinner').hide();
               }
    });
}

function ListLatestReviews()
{
    $.ajax({
               type: "GET",
               url: "/api/b/list?limit=10&offset=0",
               //url: "/reviews/scenes/listscenes?limit=2&offset=0",
               success: function(response){
                    theXmlDoc = $.parseXML(response);
                    var theRow = $(theXmlDoc).find('review').get();
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
$(function () {

    $.ajax({
               type: "GET",
               url: "/api/b/comments?reviewid="+$("#reviewid").val()+"&limit=10&offset=0",
               success: function(response){
                    oObj = $.parseJSON(response);
                    if (oObj.curuserreview) {
                   		$('#curEditContainer').show();
                   		$('#curEditContainer').find('textarea').val(oObj.curuserreview.review);
                   		$('#curEditContainer').find('#rid').val(oObj.curuserreview.reviewid);
                   		$("#curEditContainer").find('#curcreatorname').html(oObj.curuser.username);
                   	    $("#curEditContainer").find('#curcreatoravatar').attr('src',oObj.curuser.avatar);
                   	    $("#curEditContainer").find('#rating').val(oObj.curuserreview.rating);
                    }
                    else
                    {
                   		$('#curContainer').show();
                   		$("#curContainer").find('#curcreatorname').html(oObj.curuser.username);
                    	$("#curContainer").find('#curcreatoravatar').attr('src',oObj.curuser.avatar);
                    }
                    i = 0;
                    (oObj.reviews).forEach(function(eachRev) 
                    {
                        i++;
	                        var klon = $("#reviewItem" );
	                        var container = $('#revContainer');
	                        var oClone = klon.clone();
	                        $(oClone).find('#creatorname').html(eachRev.username);
	                        $(oClone).find('#creatoravatar').attr('src',eachRev.avatar);
	                       $(oClone).find('#creatordescription').html(eachRev.review);
	                       if(eachRev.rating == 1)
	                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_1_0.png');
	                       if(eachRev.rating == 1.5)
	                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_1_5.png');
	                       if(eachRev.rating == 2)
	                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_2_0.png');
	                       if(eachRev.rating == 2.5)
	                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_2_5.png');
	                       if(eachRev.rating == 3)
	                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_3_0.png');
	                       if(eachRev.rating == 3.5)
	                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_3_5.png');
	                       if(eachRev.rating == 4)
	                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_4_0.png');
	                       if(eachRev.rating == 4.5)
	                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_4_5.png');
	                       if(eachRev.rating == 5)
	                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_5_0.png');
	                        $(container).prepend('<div class = "separator"></div>');
	                        $(container).prepend(oClone);
	                        $(oClone).show();
	                      
                    });
                   

               }
    });
});
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