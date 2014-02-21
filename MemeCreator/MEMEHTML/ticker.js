var m_strCurTimeStamp = "";
setInterval(function() {
    $.ajax({
        url: "/api/oh/list?offset=0&limit=1",
        type: 'GET',
        crossDomain: true,
        
    }).done(function ( data ) {
	   theXmlDoc = data;
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
}, 5000); //5 seconds
