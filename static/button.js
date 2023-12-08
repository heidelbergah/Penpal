var drawButton = $("#draw")
drawButton.click(function(){
    $.ajax({
        url: "/draw_image",
        type: "post",
        success: function(response){
            console.log("drawing image")
        }
    });
});

var danceButton = $("#dance")
danceButton.click(function(){
    $.ajax({
        url: "/dance",
        type: "post",
        success: function(response){
            console.log("Dancing!")
        }
    });
});
