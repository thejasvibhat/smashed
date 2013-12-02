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
                    $(oClone).find('#creatorname').html($("#curcreatorname").val());
                    $(oClone).find('#creatoravatar').attr('src',$("#curcreatorname").attr('src'));
                   $(oClone).find('#creatordescription').html($("#curdescription").val());
                   if($("#rating").val() == 1)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_1.png');
                   if($("#rating").val() == 1.5)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_1_5.png');
                   if($("#rating").val() == 2)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_2.png');
                   if($("#rating").val() == 2.5)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_2_5.png');
                   if($("#rating").val() == 3)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_3.png');
                   if($("#rating").val() == 3.5)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_3_5.png');
                   if($("#rating").val() == 4)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_4.png');
                   if($("#rating").val() == 4.5)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_4_5.png');
                   if($("#rating").val() == 5)
                       $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_5.png');
                    $(container).prepend('<div class = "separator"></div>');
                    $(container).prepend(oClone);
                    $(oClone).show();


               }
    });
}

function ListPromoScenes()
{
    $.ajax({
               type: "GET",
               url: "/reviews/scenes/listscenes?limit=10&offset=0",
               //url: "/reviews/scenes/listscenes?limit=2&offset=0",
               success: function(response){
                    theXmlDoc = $.parseXML(response);
                    var theRow = $(theXmlDoc).find('review').get();
                    $(theRow).each(function(i) 
                    {
                        i++;
                        var review_name = $(this).find('name').text();
                        var imgUrl = $(this).find('icon1').text();
                        var url    =  $(this).find('url').text();
                        $('#gallery-list-reviews').find('#item_'+i).find('img').attr('src',imgUrl);
                        $('#gallery-list-reviews').find('#item_'+i).find('h6').html(review_name);
                        
                        $('#gallery-list-reviews').find('#item_'+i).click(function()
                        {
                            window.location =  url;
                        });                                                      
                    });
                   
                   $('#listReviewsLoaded').val("true");

               }
    });
}
function ListPromoMemes()
{
    $.ajax({
               type: "GET",
               url: "/meme/actions/listmeme?limit=10&offset=0",
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
                   
                   $('#listMemesLoaded').val("true");

               }
    });
}
$(function () {

    $.ajax({
               type: "GET",
               url: "/api/b/comments?reviewid="+$("#reviewid").val()+"&limit=10&offset=0",
               success: function(response){
                    oObj = $.parseJSON(response);
                   $("#curContainer").find('#curcreatorname').html(oObj.currentuser);
                   $("#curContainer").find('#curcreatoravatar').attr('src',oObj.currentavatar);

                    (oObj.reviews).forEach(function(eachRev) 
                    {
                        var klon = $("#reviewItem" );
                        var container = $('#revContainer');
                        var oClone = klon.clone();
                        $(oClone).find('#creatorname').html(eachRev.username);
                        $(oClone).find('#creatoravatar').attr('src',eachRev.avatar);
                       $(oClone).find('#creatordescription').html(eachRev.review);
                       if(eachRev.rating == 1)
                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_1.png');
                       if(eachRev.rating == 1.5)
                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_1_5.png');
                       if(eachRev.rating == 2)
                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_2.png');
                       if(eachRev.rating == 2.5)
                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_2_5.png');
                       if(eachRev.rating == 3)
                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_3.png');
                       if(eachRev.rating == 3.5)
                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_3_5.png');
                       if(eachRev.rating == 4)
                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_4.png');
                       if(eachRev.rating == 4.5)
                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_4_5.png');
                       if(eachRev.rating == 5)
                           $(oClone).find('#creatorrating').attr('src','/reviewhtml/assets/rate_5.png');
                        $(container).prepend('<div class = "separator"></div>');
                        $(container).prepend(oClone);
                        $(oClone).show();
                    });
                   

               }
    });
});
