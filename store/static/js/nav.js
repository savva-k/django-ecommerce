$(document).ready(function() {
    $('.nav-js-category-children').hide();
    $('.nav-js-category-link').click(function(event){
        event.preventDefault();
        $(this).next('.nav-js-category-children').toggle();
    });
});