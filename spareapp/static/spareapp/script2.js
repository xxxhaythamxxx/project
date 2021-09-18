$("#contCatIng").change(function(){
    if($(this).find("option:selected").attr("limit") == "True"){
        $("#divFechaTope").show()
    }
    else{
        $("#divFechaTope").hide()
    }
})

$("#contCatEgr").change(function(){
    if($(this).find("option:selected").attr("limit") == "True"){
        $("#divFechaTope").show()
    }
    else{
        $("#divFechaTope").hide()
    }
})

function functionByDay(){
    $("#formByDay").show()
    $("#formByRange").hide()
}

function functionByRange(){
    $("#formByRange").show()
    $("#formByDay").hide()
}