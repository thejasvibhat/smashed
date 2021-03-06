$(document).ready(function() {
	/*
	Dropdown
	=========================== */
	$('ul li.dropdown').hover(function () {
			$(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn();
		}, function () {
			$(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut();
	});
	
	/*
	Mobile navigation
	=========================== */
    //build dropdown
    $("<select />").appendTo(".navbar .nav-collapse .nav");
 
   
    $("<option />", {
       "selected": "selected",
       "value"   : "",
       "text"    : "Select menu"
    }).appendTo(".navbar .nav-collapse .nav select"); 
 
    //Menu items
    $(".navbar .nav-collapse .nav li a").each(function() {
        var el = $(this);
        $("<option />", {
            "value"   : el.attr("href"),
            "text"    : el.text()
        }).appendTo(".navbar .nav-collapse .nav select");
    });
 
    //Link
    $(".navbar .nav-collapse .nav select").change(function() {
        window.location = $(this).find("option:selected").val();
    });
	
});


$(window).load(function()
{
	$('.frontImages img').click(function()
	{
		$('#i'+$(this).attr('id')).click();
	});
	
	$('input[type="file"]').on('change',function(input)
	{
		var id = $(this).attr('id').replace('i','');
		readURL(input,id);  	
	});
	
	$('#uploadReviewForm').submit(function(event)
	{
		
		if( !$("#uploadReviewForm").validationEngine('validate'))
		{
			return false;
		}
		//event.preventDefault();
		$('#uploadSpinner').fadeIn();
	});
	
});

function readURL(input,id) {
	var file = input.target.files[0];
    var reader = new FileReader();
    
    reader.readAsDataURL(file);
    reader.onloadend = function(e) {
    	$('#'+id).attr('src', e.target.result);          
    } 
}

function uploadReviewInit()
{

	$('#nav-review-record').addClass ('nav-highlight');

	/* Steppers */	
	$('#rating').stepper({
    	wheel_step:0.5,       // Wheel increment is 1
    	limit: [1,5],         // No negative values
    	onStep: function( val, up )
    	{
        	// do something here...
    	}
	});
	
	$('#uploadReviewForm').validationEngine({promptPosition : "topLeft", scroll: false});
	
	/* Address Picker */
	
	var addresspickerMap = $( "#addresspicker_map" ).addresspicker({
	regionBias: "in",
    updateCallback: showCallback,
	elements: {
		    map:      "#map",
		    lat:      "#lat",
		    lng:      "#lng",
		    street_number: '#street_number',
		    route: '#route',
		    locality: '#locality',
		    administrative_area_level_2: '#administrative_area_level_2',
		    administrative_area_level_1: '#administrative_area_level_1',
		    country:  '#country',
		    postal_code: '#postal_code',
        	type:    '#type' 
		  }
	});
	
	$("#addresspicker_map").addresspicker("option", "reverseGeocode","true");

	var gmarker = addresspickerMap.addresspicker( "marker");
	gmarker.setVisible(true);
	addresspickerMap.addresspicker( "updatePosition");

    function showCallback(geocodeResult, parsedGeocodeResult){
      //?
    }
	
	
}

function stickFooter ()
{
	var $footer = $(".footer");
    positionFooter();

   function positionFooter() {

          if ( $(document.body).height() < $(window).height() ) {
               $footer.css({
                    position: "fixed",
                    bottom: 0,
                    left:0,
                    right:0
               })
           } else {
               $footer.attr("style", "");
           }

   }
   $(window).resize(positionFooter);
}

function uploadReviewAutoCompleteArea()
{
		$('#location').keyup(function()
		{
			$.ajax({
                type: 'GET',
                dataType:'json',
                url: '/api/b/ajaxlist?search='+$(this).val(),
                success: function(responseData) {
                
                $( "#location" ).autocomplete(
				{
		 			source:responseData.results
				});
                
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                        //TODO
                }
       		 }); 

		});
}

function BInit()
{
	$('#bSearch').show();
	$('#nav-reviews').addClass ('nav-highlight');
	$('#curContainer').find('#rating').stepper({
    	wheel_step:0.5,       // Wheel increment is 1
    	limit: [1,5],         // No negative values
    	onStep: function( val, up )
    	{
        	// do something here...
    	}
	});
	$('#curEditContainer').find('#rating').stepper({
    	wheel_step:0.5,       // Wheel increment is 1
    	limit: [1,5],         // No negative values
    	onStep: function( val, up )
    	{
        	// do something here...
    	}
	});
	$('#bSearchInput').live("keyup",function(event)
	{
		getBarListing($(this).val());
	});
	/* Get OverHeards */
	$.ajax({
            type: 'GET',
            url: '/api/b/overheards?bid='+$('#bid').val(),
            success: getBarOverHeards,
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                        //TODO
            }
    }); 
    
    
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
                   	    $('#curEditContainer').find('#descreview').val(oObj.curuserreview.desreview);
                    }
                    else
                    {
                   		$('#curContainer').show();
                   		$("#curContainer").find('#curcreatorname').html(oObj.curuser.username);
                    	$("#curContainer").find('#curcreatoravatar').attr('src',oObj.curuser.avatar);
                    }
                    (oObj.reviews).forEach(function(eachRev) 
                    {
                        	if (eachRev.desreview != "1") {
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
							}
	                      
                    });
                   

               }
    });
    
	
}

function getBarOverHeards(data)
{
	theXmlDoc = $.parseXML(data);
    var theRow = $(theXmlDoc).find('meme').get();
    $(theRow).each(function(i)
    {
    	i++;
    	var icon = $(this).find("icon").text();
    	var ele  = $('#bOhIndvTpl').clone().attr('id','bOhIndv_'+i);
    	$(ele).find('img').attr('src',icon);
    	$(ele).find('a').attr('href',icon);
    	$('#OhAtContainer').append(ele);
    	$(ele).show();
    });
}

function reviewsInit()
{
                	 $( "#bSearchInput" ).autocomplete({
					minLength: 0,
					source: null,
					focus: function( event, ui ) {
						$( "#bSearchInput" ).val( ui.item.name );
						return true;
					},
					select: function( event, ui ) {
						$( "#bSearchInput" ).val( ui.item.name );
						window.location = "/b/"+ui.item.bid;
					}
				});

	var $container = $('#c');
        $container.imagesLoaded( function(){
                $container.isotope({
                        // options
                        itemSelector : '.bIndv',
                        layoutMode   : 'masonry'
                });
        });




	$('#bSearch').show();
	$('#nav-reviews').addClass ('nav-highlight');
	$('#bSearchInput').live("keyup",function(event)
	{
		getBarListing($(this).val());
	});
}

function ohListInit()
{
	$('#nav-oh').addClass ('nav-highlight');
}
function recordOhInit()
{
	ohtype = "Conversation";	
	GridChange();
	$('#nav-oh-record').addClass ('nav-highlight');
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
}

function getBarListing(a_val)
{
	$.ajax({
            type: 'GET',
            dataType:'json',
            url: '/api/b/ajaxlist?type=bar&search='+a_val,
            success: function(responseData) {
            	 $( "#bSearchInput" ).autocomplete({
					minLength: 0,
					source: responseData.results,
					focus: function( event, ui ) {
						$( "#bSearchInput" ).val( ui.item.label );
						return true;
					},
					select: function( event, ui ) {
						$( "#bSearchInput" ).val( ui.item.name );
						window.location = "/b/"+ui.item.bid;
                        return true;
					}
				});
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                //TODO
            }
    }); 
}

/* Function to show google map */

function showBarOnMapModal (a_ele)
{
	var latlon      = $(a_ele).attr('value');
	var locationArr = latlon.split(":");
	var lat         = locationArr[0];
	var lon			= locationArr[1];
	$( "#mapModal" ).dialog({ 
		open: drawMap (lat,lon),
		modal:true,
		minWidth:400,
		resizable:false,
		draggable:false
	});
}

function drawMap (lat,lon)
{
	var myLatLng = new google.maps.LatLng(lat,lon);
    var map_canvas = document.getElementById('map_canvas');
    var map_options = {
      center: myLatLng,
       zoom: 16,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(map_canvas, map_options)
    var marker = new google.maps.Marker({
 		position: myLatLng,
  		map: map
	}); 
	
}

/* Share on social Networks */

function shareOhOnFaceBook (a_id,type)
{
    var shareurl = 'http://www.facebook.com/sharer.php?u=';
    if(type == 'private')
        shareurl = shareurl +  'http://www.smashed.in/oh/'+a_id;
    else
        shareurl = shareurl +  a_id;
	shareSocial(shareurl);
}

function shareOhOnTwitter (a_id)
{
	var text = "Check out this cool OverHeard";
	shareSocial('http://www.twitter.com/share?url=http://www.smashed.in/oh/'+a_id+'&text='+text+'&counturl=/oh/'+a_id+'&hashtags=smashed,overheards,fun,scene,core');
	
}

function shareOhOnGoogle (a_id)
{
	shareSocial('https://plus.google.com/share?url=http://www.smashed.in/oh/'+a_id);
}

function shareSocial (a_url)
{
	window.open( a_url, "Smashed", "status = 1, height = 350, width =650, resizable = 0" );
}

function Login()
{
	window.location = "/auth";
}

function setRedirectUrl(a_ele)
{
	$(a_ele).attr('href','/auth?redirect_url='+window.location.href);
	$(a_ele).click();
}
	
function LandingInit()
{
	/*
	var height = $(window).height();
	var margin = height / 2 - 140;
	$('#landingText').css('margin-top',margin+'px');
	*/
	if(navigator.userAgent.toLowerCase().indexOf("android") > -1) {
    	window.location.href= "market://details?id=com.smashedin.smashedin";
	}
}

