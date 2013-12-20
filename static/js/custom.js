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
	$('#bSearchInput').live("keyup",function(event)
	{
		getBarListing($(this).val());
	});
}

function reviewsInit()
{

	$('#c').isotope({
		itemSelector : '.bIndv',
    	layoutMode   : 'masonry'
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
	var sourceone = ["fuck","you"];
	$.ajax({
            type: 'GET',
            dataType:'json',
            url: '/api/b/ajaxlist?type=bar&search='+a_val,
            success: function(responseData) {
            	 $( "#bSearchInput" ).autocomplete({
					minLength: 0,
					source: responseData.results,
					focus: function( event, ui ) {
						$( "#bSearchInput" ).val( ui.item.name );
						return false;
					},
					select: function( event, ui ) {
						$( "#bSearchInput" ).val( ui.item.name );
						window.location = "/b/"+ui.item.bid;
					}
				})
					.data( "ui-autocomplete" )._renderItem = function( ul, item ) {
					return $( "<li>" )
					.append( "<a>" + item.name + "<br>" + item.locality + "</a>" )
					.appendTo( ul );
				};
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

function shareOhOnFaceBook (a_id)
{
	
}

function shareOhOnTwitter (a_id)
{
	
}

function shareOhOnGoogle (a_id)
{
	
}
		

