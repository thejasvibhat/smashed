function ListComments()
{
    $.ajax({
               type: "GET",
               url: "/api/oh/comments?commentid="+$("#commentid").val()+"&limit=10&offset=0",
               success: function(response){
                    oObj = $.parseJSON(response);
                   $("#curContainer").find('#curcreatorname').html(oObj.currentuser);
                   $("#curContainer").find('#curcreatoravatar').attr('src',oObj.currentavatar);
                    
                    (oObj.comments).forEach(function(eachCom) 
                    {
                        if(eachCom.commentid != $("#commentid").val())
                        {
                            var klon = $("#commentItem" );
                            var container = $('#comContainer');
                            var oClone = klon.clone();
                            $(oClone).find('#creatorname').html(eachCom.username);
                            $(oClone).find('#creatoravatar').attr('src',eachCom.avatar);
                           $(oClone).find('#creatordescription').html(eachCom.comment);
                            $(container).prepend('<div class = "separator"></div>');
                            $(container).prepend(oClone);
                            $(oClone).show();
                        }
                    });
                   

               }
    });
}
function SaveComments()
{
    var data = {'comment': $("#curdescription").val(),'commentid':$('#commentid').val()};
     $.ajax({
               type: "GET",
               url: "/api/oh/updatecomment",
               data:data,
               success: function(response){
                    var klon = $("#commentItem" );
                    var container = $('#comContainer');
                    var oClone = klon.clone();
                    $(oClone).find('#creatorname').html($("#curcreatorname").val());
                    $(oClone).find('#creatoravatar').attr('src',$("#curcreatorname").attr('src'));
                   $(oClone).find('#creatordescription').html($("#curdescription").val());
                    $(container).append('<div class = "separator"></div>');
                    $(container).append(oClone);
                    $(oClone).show();

               }
    });
}