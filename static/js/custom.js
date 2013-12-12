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
	
	/* Location Picker */
	$('#addressLocator').locationPicker();
	
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

