$(document).ready(function(){

    $(".show_comment").on("click", function () {
        if ($('.new_comment').css("display") == "none"){
            $('.new_comment').css("display", "block")
        } else {
            $('.new_comment').css("display", "none")
        }
    })
});