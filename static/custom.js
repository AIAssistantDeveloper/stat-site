$(document).ready(function(){
    // ScrollReveal animations
    ScrollReveal().reveal('header h1', { delay: 500, distance: '50px', origin: 'top' });
    ScrollReveal().reveal('header p', { delay: 800, distance: '50px', origin: 'bottom' });
    ScrollReveal().reveal('.btn', { delay: 1000, distance: '50px', origin: 'bottom' });

    // Smooth scrolling for links
    $('a[href*="#"]').on('click', function(e) {
        e.preventDefault();
        $('html, body').animate({
            scrollTop: $($(this).attr('href')).offset().top
        }, 500);
    });
});