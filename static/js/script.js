var lnStickyNavigation;

$(document).ready(function()
{	
	applyHeader();
	applyNavigation(); 
	applyResize();

});

/* HEADER FUNCTIONS */

function applyHeader()
{
	$('.jumbotron').css({ height: ($(window).height()) +'px' });
	
	
}	



/* NAVIGATION FUNCTIONS */

function applyNavigation()
{
	applyClickEvent();
	applyNavigationFixForPhone();
	applyScrollSpy();
	applyStickyNavigation();
}

function applyClickEvent()
{
	$('a').on('click', function(e)
	{
		e.preventDefault();
		
		if( $( $.attr(this, 'href') ).length > 0 )
		{
			$('html, body').animate(
			{
				scrollTop: $( $.attr(this, 'href') ).offset().top
			}, 400);
		}
		return false;
	});
}

function applyNavigationFixForPhone()
{
	$('.navbar li a').click(function(event) 
	{
		$('.navbar-collapse').removeClass('in').addClass('collapse');
	});
}

function applyScrollSpy()
{
	$('#navbar-example').on('activate.bs.scrollspy', function() 
	{
		window.location.hash = $('.nav .active a').attr('href').replace('#', '#/');
	});
}

function applyStickyNavigation()
{
	lnStickyNavigation = $('.scroll-down').offset().top + 20;
	
	$(window).on('scroll', function() 
	{  
		stickyNavigation();  
	});  
	
	
}

function stickyNavigation()
{         
	if($(window).scrollTop() > lnStickyNavigation) 
	{   
		$('body').addClass('fixed');  
	} 
	else 
	{  
		$('body').removeClass('fixed');   
	}  
}



/* RESIZE FUNCTION */

function applyResize()
{
	$(window).on('resize', function() 
	{  
		lnStickyNavigation = $('.scroll-down').offset().top + 20;
	
		$('.jumbotron').css({ height: ($(window).height()) +'px' });
	}); 
}


