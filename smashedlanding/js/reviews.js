var myname = "naren";
function ListPromoScenes()
{
    $.ajax({
               type: "GET",
               url: "http://localhost:8080/reviews/scenes/listscenes?limit=2&offset=0",
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

               }
    });
}
