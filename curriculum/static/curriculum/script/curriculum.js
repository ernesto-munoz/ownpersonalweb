$(document).ready(function(){
    $("#img_project01").click(function(){
        hideAll()
        $("#project01").show("fast");
    });

    $("#img_project02").click(function(){
        hideAll()
        $("#project02").show("fast");
    });
});

function hideAll(){
    $("#project01").hide();
    $("#project02").hide();
}