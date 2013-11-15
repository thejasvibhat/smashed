var myname = "naren";
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
                            window.location = "http://localhost:8080" + url;
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
                            window.location = "http://localhost:8080" + url;
                        });                                                      
                    });
                   
                   $('#listMemesLoaded').val("true");

               }
    });
}
