// Función para enlazar los selects -----------------------------------------------------------------------------
const $carro = $("#car_id");
const $modelo = $("#car_model_id");
const $motor = $("#engine_id");

$carro.change(function(){
    $modelo.val('');
    
    $modelo.prop('disabled', !Boolean($carro.val()));
    $motor.prop('disabled', !Boolean($modelo.val()));
    $modelo.find('option[data-carro]').hide();
    $modelo.find('option[data-carro="' + $carro.val() + '"]').show();
    
});

$modelo.change(function(){
    $motor.val('');
    
    $motor.prop('disabled', !Boolean($modelo.val()));
    $modelo.prop('disabled', !Boolean($carro.val()));
    $motor.find('option[data-carro]').hide();
    $motor.find('option[data-carro="' + $modelo.val() + '"]').show();
    
});

// Funcion filtrar -----------------------------------------------------------------------------------------------
$(document).ready(function(){
    $("#myInput").on("keyup",function(){                                // Cuando se teclea algo
        var value = $(this).val().toLowerCase();                        // Toma el valor del input en minuscula
        $("#myTable tr").filter(function(){                             // 
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        })
    })
});
var listado = []
var listadoAll = 0
var table = "#invoice"
listadoPasar = [] 
var listadoCategory = []
var listadoVendor = []
var contCategory = []
var pasarCategory = []
var compVendors = []
var contVendor = []
var compCategories = []
var contTotalTable = []


// Funcion para filtrar por medidas y atributos -------------------------------------------------------------------
function measureFilter(){

    // listado = []
    listadoAll = 0

    $("#myTable tr").each(function(){
        $(this).hide();
    })

    $(".filterDim").each(function(){
        var indexVal = $(this).attr("id")                           // id = DiameterFilter
        // alert(indexVal)
        var atribute = indexVal.split("Filter")                     // Dim8, - Dim2, - LaDimension,
        // alert(atribute)
        var dimAtribute = atribute[0]                               // Diameter - Height - Atr1
        // alert("dimAtribute: "+dimAtribute)
        var AtributeMin
        var AtributeMax
        var AtributeString
        
        $(this).find("input").each(function(){
            var comp = $(this).val().toLowerCase()                                // 1 - 5 - off - on
            if(comp){
                listadoAll++
            }
            var innerAtribute = $(this).attr("id").split("Min")[0]  // Diameter - Height - Atr1
            if(!($(this).attr("id").split("Min")[1]=="" || $(this).attr("id").split("Max")[1]=="")){
                AtributeString = comp                       // on - off
                if(AtributeString!=""){
                    listadoAll++
                }
            }
            if(dimAtribute === innerAtribute){
                AtributeMin = comp
            }else{
                AtributeMax = comp
            }
        })

        // $(".cantainer").each(function(){
        //     alert($(this).text())
        //     $(this).find("div").each(function(){
        //         // alert($(this).text())
        //     })
        // })

        $('#myTable tr a').each(function(){
            if($(this).attr("id")===(dimAtribute+"Value")){
                $(this).find(".cantainer").each(function(){
                    var varSplit = $(this).find("#AtrName").text()
                    var valor = $(this).find("#AtrVal").text()      // 88.0 mm - on - FOAM
                    aux = valor.split(" mm")
                    if(aux.length>1){
                        var VarFloat = parseFloat(valor)
                    }else{
                        var varString = valor
                    }
                    if(AtributeMin<=VarFloat & AtributeMax>=VarFloat){  // Almaceno en listado las dimensiones que se encuentren en el rango
                        indexDiameter=$(this).text()
                        listado.push(indexDiameter)
                    }

                    if(AtributeString){
                        if(varString.toLowerCase().indexOf(AtributeString.toLowerCase()) > -1){
                            indexDiameter=$(this).text()
                            listado.push(indexDiameter)
                        }
                    }
                })
            }
        })

        // ----------------------------------------------------------
        // $('#myTable tr a').each(function(){
        //     if($(this).attr("id")===(dimAtribute+"Value")){
        //         // alert($(this).attr("id"))
        //         // alert("Nuevo: "+$(this).text())
        //         var text = $(this).text();                          // Diameter 40.5 mm - Atr1 off
        //         // alert($(this).text())         // Dim888.0 mm
        //         $(this).find("#AtrName").each(function(){
        //             alert($(this).text())
        //         })
        //         if($(this))
        //         var varSplit = text.split(": ")[1]                  // Ya no sirve
        //         // alert(varSplit)
        //         var auxS = text.split(" ")                          // Dim8,88.0,mm - Uno,dos,3131.0,mm - material,FOAM
        //         // alert(auxS)
        //         if(auxS[auxS.length-1] == "mm"){ // si es una dimension
        //             var auxSS = text.split(auxS[auxS.length-2])     // Dim8 , mm - Dim2 , mm
        //             // alert(auxSS)
        //             var varSplit = text.split(auxSS[0])             // ,88.0 mm - ,22.0 mm
        //             // alert(varSplit)
        //             varSplit = varSplit[1].split(" ")
        //             var VarFloat = parseFloat(varSplit[0])              // 88 - 40 (Float)
        //             // alert(VarFloat)
        //         }else{                              // si es un atributo
        //             var auxSS = text.split(auxS[auxS.length-1])        // material , - El Atr , - Atr ,
        //             // alert(auxSS)
        //             var varSplit = text.split(auxSS[0])             // ,FOAM - ,down - ,on
        //             // alert(varSplit)
        //             var varString = varSplit[1].toLowerCase()        // foam - down - on (String)
        //             // alert(varString)
        //         }
                // if(AtributeMin<=VarFloat & AtributeMax>=VarFloat){  // Almaceno en listado las dimensiones que se encuentren en el rango
                //     indexDiameter=$(this).text()
                //     listado.push(indexDiameter)
                // }
                
                // if(AtributeString){
                //     if(varString.indexOf(AtributeString) > -1){
                //         indexDiameter=$(this).text()
                //         listado.push(indexDiameter)
                //     }
                // }
        //     }
        // })
        // ----------------------------------------------------------

    })

    // alert(listado)
    for(var i = listado.length -1; i >=0; i--){
        if(listado.indexOf(listado[i]) !== i) listado.splice(i,1);
    }
    // alert(listado)               // Guarda cuando consigue un atributo: Atron
                                    // Si consigue 2: Atron,El Atrdown

    listadoAll=listadoAll/2

    // alert(listadoAll)

    for(var i=0; i<listado.length; i++){            // Recorro para volver a numerar
        $("#myTable tr").each(function(){
            $(this).find("td").each(function(){
                if($(this).index()===$("#detail-id").index()){
                    if($(this).parent().is(":visible")){
                        // alert($(this).text())
                        $(this).text(""+(i+1)+"")
                        i=i+1;
                    }
                }
            })
        })
    }

    // Paginado
    $(".pagination").html("")
    var trnum = 0
    // Guarda la cantidad de filas seleccionadas
    var maxRows = parseInt($("#maxRows").val())
    var semiTotalRows = $(table+" tbody tr").length
    totalRows = listado.length
    var rev = false
    var is = false
    var listCont = 0
    var aCont = 0
    $("tbody tr").each(function(){
        trnum++
        $(this).find("td").each(function(){
            $(this).find("a").each(function(){
                // alert("Cada a: "+$(this).text())
                if($(this).parent().parent().index()==$("#dimensions").index() || $(this).parent().parent().index()==$("#atributes").index()){
                    aCont++
                    // alert("Columna: "+$(this).text())
                    for(var i=0; i<listado.length; i++){
                        // alert("Val a: "+$(this).text()+" con listado: "+listado[i])
                        if($(this).text()==listado[i]){
                            // alert("Cada a: "+$(this).text())
                            listCont++
                        }else{
                            is = false
                        }
                    }

                }

            })
        })
        // alert("listCont: "+listCont+" listadoAll: "+listadoAll+" listadoLeng: "+listado.length)
        if((listCont == listadoAll) && (listCont>0)){
            is = true
        }else{
            is = false
        }
        if(is == true){
            rev = true
            if(trnum > maxRows){
                $(this).hide()
            }
            if(trnum <= maxRows){
                $(this).show()
            }
        }
        if(rev===false){
            trnum--
        }else{
            rev = false
        }
        is = true
        listCont = 0
    });
    // Antes de ésto es que debe filtrar las categorias checkeadas
    if(totalRows > maxRows){
        // Guardo la cantidad de paginas que se necesitan
        var pagenum = Math.ceil(totalRows/maxRows)
        for(var i=1;i<=pagenum;){
            $(".pagination").append('<li class="page-item" data-page="'+i+'"><a class="page-link" href="#"><span>'+ i++ +'<span class="sr-only">(current)</span></span></a></li>').show()
        }
    }
    $(".pagination li:first-child").addClass("active")
    $(".pagination li").on("click",function(){
        // alert("Paginacion")
        var pageNum = $(this).attr("data-page")
        var trIndex = 0;
        var rev = false
        $(".pagination li").removeClass("active")
        $(this).addClass("active")
        // Recorre tolas las filas de la tabla
        $(table+" tr:gt(0)").each(function(){
            trIndex++
            $(this).find("a").each(function(){
                for(var i=0; i<listado.length; i++){

                    if($(this).text()===listado[i]){
                        rev = true

                        if(trIndex > (maxRows*pageNum) || trIndex <= ((maxRows*pageNum)-maxRows)){
                            $(this).parent().parent().parent().hide()
                        }else{
                            $(this).parent().parent().parent().show()
                        }
                    }
                }
            })
            if(rev===false){
                trIndex--
            }else{
                rev = false
            }

        })
    })
    // Fin paginado
// alert(listado)      // Atron,El Atrdown,materialFOAM,Dim222.0 mm
// listadoPasar = listado.slice()
for(var x = 0;x < listado.length; x++){
    listadoPasar.push(listado[x])
}
}
// alert(listado)
// alert(listadoPasar)
// $(".dimMin").on('keyup', function (e) {
//     alert("Entra")
//     if (e.key === 'Enter' || e.keyCode === 13) {
//         measureFilter()
//     }
// })

$(function(){

    $(".dimMin").keyup(function (e) {
        if (e.keyCode === 13) {
            measureFilter()
        }
     })

     $(".dimMax").keyup(function (e) {
        if (e.keyCode === 13) {
            measureFilter()
        }
     })

     $(".atrUnique").keyup(function (e) {
        if (e.keyCode === 13) {
            measureFilter()
        }
     })
})

// Funcion resetear valores del filtro de medidas ---------------------------------------------------
function measureReset(){

    $("#headerList2").each(function(){
        $(this).find("input").each(function(){
            var aux = $(this).attr("name").split("check")[1]
            $("#"+aux+"Min").val(null);
            $("#"+aux+"Max").val(null);
        })
    })
    $("#headerList3").each(function(){
        $(this).find("input").each(function(){
            var aux = $(this).attr("name").split("check")[1]
            $("#"+aux).val(null);
        })
    })

    $("#myTable tr").each(function(){
        $(this).show();
    })

    // Arreglar numeros de ID
    var i = 1;
    $("tbody tr").each(function(){
        $(this).find("td").each(function(){
            if($(this).index()==$("#detail-id").index()){
                $(this).text(i);
                i=i+1;
            }
            
        })
    });

    listado = []
    // Paginacion
    $(".pagination").html("")
    var trnum = 0
    var maxRows = parseInt($("#maxRows").val())
    var totalRows = $(table+" tbody tr").length
    $(table+' tr:gt(0)').each(function(){
        trnum++
        if(trnum > maxRows){
            $(this).hide()
        }
        if(trnum <= maxRows){
            $(this).show()
        }
    })
    if(totalRows > maxRows){
        var pagenum = Math.ceil(totalRows/maxRows)
        for(var i=1;i<=pagenum;){
            $(".pagination").append('<li class="page-item" data-page="'+i+'"><a class="page-link" href="#"><span>'+ i++ +'<span class="sr-only">(current)</span></span></a></li>').show()
        }
    }
    $(".pagination li:first-child").addClass("active")
    $(".pagination li").on("click",function(){
        var pageNum = $(this).attr("data-page")
        var trIndex = 0;
        $(".pagination li").removeClass("active")
        $(this).addClass("active")
        $(table+" tr:gt(0)").each(function(){
            trIndex++
            if(trIndex > (maxRows*pageNum) || trIndex <= ((maxRows*pageNum)-maxRows)){
                $(this).hide()
            }else{
                $(this).show()
            }
        })
    })
    // fin paginacion
}

// Generar PDF desde HTML ----------------------------------------------------------------------------------------
function generatePDF(){
    var oldCss = {
        "background-size": "80px 80px",
        "width": "80px",
        "height": "80px"
    }
    $("#myTable tr").each(function(){
        $(this).find(".photo").each(function(){
            $(this).css(oldCss);
        })
    })
    $('#invoice tr:first th').each(function() {
        var value = $(this).css("position", "static");
      });
    const element = document.getElementById("invoice");
    $("#check").hide();
    $("table td:nth-child("+($("#check").index() + 1)+")").hide();
    
    var opt = {
        margin:       1,
        filename:     'report.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        enableLinks:  false,
        pagebreak:    {mode: "avoid-all"},
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'landscape' }
      };
    html2pdf()
    .set(opt)
    .from(element)
    .save();
    html2pdf().set(opt).from(element).toPdf().get('pdf').then(function (pdf) {
        $('#invoice tr:first th').each(function() {
            var value = $(this).css("position", "sticky");
            $("#check").show();
            $("table td:nth-child("+($("#check").index() + 1)+")").show();
            $("input:checkbox[name=check]").prop("checked",true);
          });
      });
}

// Visualizar para imprimir --------------------------------------------------------------------------------------
function viewPDF(){
    var oldCss = {
        "background-size": "80px 80px",
        "width": "80px",
        "height": "80px"
    }
    $("#myTable tr").each(function(){
        $(this).find(".photo").each(function(){
            $(this).css(oldCss);
        })
    })
    const element = document.getElementById("invoice");
    
    $("#check").hide();
    $("table td:nth-child("+($("#check").index() + 1)+")").hide();
    $('#invoice tr:first th').each(function() {
        var value = $(this).css("position", "static");
      });
    var opt = {
        margin:       0.5,
        filename:     'report.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        enableLinks:  true,
        pagebreak:    {mode: "avoid-all"},
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'landscape' }
      };
    html2pdf()
    .set(opt)
    .from(element);
    
    html2pdf().set(opt).from(element).toPdf().get('pdf').then(function (pdf) {
        window.open(pdf.output('bloburl'), '_blank');
        $('#invoice tr:first th').each(function() {
            var value = $(this).css("position", "sticky");
            $("#check").show();
            $("table td:nth-child("+($("#check").index() + 1)+")").show();
            $("input:checkbox[name=check]").prop("checked",true);
          });
      });
}

// Función para que los checkboxes se seleccionen todos ------------------------------------------------------------

function toggle(source,toAdd) {
    checkboxes = document.getElementsByName(toAdd);
    for (var i = 0,
        n = checkboxes.length; i < n; i++) {
        checkboxes[i].checked = source.checked;
    }
}

function toggle(source,toDel) {
    checkboxes = document.getElementsByName(toDel);
    for (var i = 0,
        n = checkboxes.length; i < n; i++) {
        checkboxes[i].checked = source.checked;
    }
}


// Boton default para que reinicie la tabla ------------------------------------------------------------------------
document.getElementById("default").addEventListener("click",function(){
    $("input:checkbox[name=photo]").prop("checked",true);
    $("input:checkbox[name=code]").prop("checked",true);
    $("input:checkbox[name=brand]").prop("checked",true);
    $("input:checkbox[name=type]").prop("checked",true);
    $("input:checkbox[name=shape]").prop("checked",false);
    $("input:checkbox[name=dimensions]").prop("checked",true);
    $("input:checkbox[name=atributes]").prop("checked",true);
    $("input:checkbox[name=category]").prop("checked",true);
    $("input:checkbox[name=priceM]").prop("checked",false);
    $("input:checkbox[name=priceD]").prop("checked",false);
    $("input:checkbox[name=car]").prop("checked",true);
    $("input:checkbox[name=check]").prop("checked",true);
    $("input:checkbox[name=reference]").prop("checked",true);
    $("input:checkbox[name=ecode]").prop("checked",true);
    $("#headerList2").each(function(){
        $(this).find("input").each(function(){
            var comp = $(this).attr("name")
            $(this).prop("checked",false);
        })
    })
    $("#headerList3").each(function(){
        $(this).find("input").each(function(){
            var comp = $(this).attr("name")
            $(this).prop("checked",false);
        })
    })

    $("#photo").show();
    $("table td:nth-child("+($("#photo").index() + 1)+")").show();
    $("#priceM").hide();
    $("table td:nth-child("+($("#priceM").index() + 1)+")").hide();
    $("#priceD").hide();
    $("table td:nth-child("+($("#priceD").index() + 1)+")").hide();
    $("#code").show();
    $("table td:nth-child("+($("#code").index() + 1)+")").show();
    $("#brand").show();
    $("table td:nth-child("+($("#brand").index() + 1)+")").show();
    $("#type").show();
    $("table td:nth-child("+($("#type").index() + 1)+")").show();
    $("#car").show();
    $("table td:nth-child("+($("#car").index() + 1)+")").show();
    $("#check").show();
    $("table td:nth-child("+($("#check").index() + 1)+")").show();
    $("#shape").hide();
    $("table td:nth-child("+($("#shape").index() + 1)+")").hide();
    $("#dimensions").show();
    $("table td:nth-child("+($("#dimensions").index() + 1)+")").show();
    $("#atributes").show();
    $("table td:nth-child("+($("#atributes").index() + 1)+")").show();
    $("#reference").show();
    $("table td:nth-child("+($("#reference").index() + 1)+")").show();
    $("#category").show();
    $("table td:nth-child("+($("#category").index() + 1)+")").show();
    $("#ecode").show();
    $("table td:nth-child("+($("#ecode").index() + 1)+")").show();
    $("#headerList2").each(function(){
        $(this).find("input").each(function(){

            var aux = $(this).attr("name").split("check")[1]
            $("#"+aux+"Filter").hide();
        })
    })
    $("#headerList3").each(function(){
        $(this).find("input").each(function(){

            var aux = $(this).attr("name").split("check")[1]
            $("#"+aux+"Filter").hide();
        })
    })
    $("#ButtonFilter").hide();

    $("#myTable tr").each(function(){
        $(this).show();
    })
    measureReset();
})

// boton para exportar a Excel -------------------------------------------------------------------------------------
document.getElementById("downloadexcel").addEventListener("click",function(){
    $("#check").hide();
    $("table td:nth-child("+($("#check").index() + 1)+")").hide();
    $("#photo").hide();
    $("table td:nth-child("+($("#photo").index() + 1)+")").hide();
    var table2excel = new Table2Excel();
    table2excel.export(document.querySelectorAll("#invoice"));
    // $("#check").show();
    // $("table td:nth-child("+($("#check").index() + 1)+")").show();
    $("input:checkbox[name=check]").prop("checked",false);
    $("input:checkbox[name=photo]").prop("checked",false);
})

// Para filtrar por dimensiones -----------------------------------------------------------------------------------
const $spname = $("#spare_name");
const $spshape = $("#spare_shape");
const $content = $("#dimensions-content");
const $long = $("#long");

$spname.change(function(){
    $spshape.val('');
    
    $spshape.prop('disabled', !Boolean($spname.val()));
    $motor.prop('disabled', !Boolean($spshape.val()));
    $spshape.find('option[data-carro]').hide();
    $spshape.find('option[data-carro="' + $spname.val() + '"]').show();
    
});
$spshape.change(function(){
    $content.hide();
    if($spshape.val()){
        $content.show();
    }
});


// Para seleccionar la cabecera de la tabla dinamicamente ------------------------------------------------------
const $HeaderB = $("#dLabel");
const $List = $("#headerList");
const $cab = 5;
$("input:checkbox[name=detail-id]").prop("checked",true);
$("input:checkbox[name=photo]").prop("checked",true);
$("input:checkbox[name=code]").prop("checked",true);
$("input:checkbox[name=brand]").prop("checked",true);
$("input:checkbox[name=type]").prop("checked",true);
$("input:checkbox[name=shape]").prop("checked",false);
$("input:checkbox[name=dimensions]").prop("checked",true);
$("input:checkbox[name=atributes]").prop("checked",true);
$("input:checkbox[name=reference]").prop("checked",true);
$("input:checkbox[name=priceM]").prop("checked",false);
$("input:checkbox[name=priceD]").prop("checked",false);
$("input:checkbox[name=car]").prop("checked",true);
$("input:checkbox[name=check]").prop("checked",true);
$("input:checkbox[name=ecode]").prop("checked",true);
$("input:checkbox[name=category]").prop("checked",true);
$("input:checkbox[name=vendor]").prop("checked",false);

$List.change(function(){

    let detailidi = $("#detail-id").index();
    let photoi = $("#photo").index();
    let codei = $("#code").index();
    let brandi = $("#brand").index();
    let typei = $("#type").index();
    let cari = $("#car").index();
    let shapei = $("#shape").index();
    let dimensionsi = $("#dimensions").index();
    let atributesi = $("#atributes").index();
    let priceDi = $("#priceD").index();
    let priceMi = $("#priceM").index();
    let referencei = $("#reference").index();
    let checki = $("#check").index();
    let ecodei = $("#ecode").index();
    let categoryi = $("#category").index();
    let vendori = $("#vendor").index();

    if ($("input:checkbox[name=detail-id]:checked").val()){
        $("#detail-id").show();
        $("table td:nth-child("+(detailidi + 1)+")").show();
    }else{
        $("#detail-id").hide();
        $("table td:nth-child("+(detailidi + 1)+")").hide();
    }

    if ($("input:checkbox[name=priceM]:checked").val()){
        $("#priceM").show();
        $("table td:nth-child("+(priceMi + 1)+")").show();
    }else{
        $("#priceM").hide();
        $("table td:nth-child("+(priceMi + 1)+")").hide();
    }

    if ($("input:checkbox[name=priceD]:checked").val()){
        $("#priceD").show();
        $("table td:nth-child("+(priceDi + 1)+")").show();
    }else{
        $("#priceD").hide();
        $("table td:nth-child("+(priceDi + 1)+")").hide();
    }

    if ($("input:checkbox[name=photo]:checked").val()){
        $("#photo").show();
        $("table td:nth-child("+(photoi + 1)+")").show();
    }else{
        $("#photo").hide();
        $("table td:nth-child("+(photoi + 1)+")").hide();
    }

    if ($("input:checkbox[name=code]:checked").val()){
        $("#code").show();
        $("table td:nth-child("+(codei + 1)+")").show();
    }else{
        $("#code").hide();
        $("table td:nth-child("+(codei + 1)+")").hide();
    }
    
    if ($("input:checkbox[name=brand]:checked").val()){
        $("#brand").show();
        $("table td:nth-child("+(brandi + 1)+")").show();
    }else{
        $("#brand").hide();
        $("table td:nth-child("+(brandi + 1)+")").hide();
    }
    
    if ($("input:checkbox[name=type]:checked").val()){
        $("#type").show();
        $("table td:nth-child("+(typei + 1)+")").show();
    }else{
        $("#type").hide();
        $("table td:nth-child("+(typei + 1)+")").hide();
    }

    if ($("input:checkbox[name=car]:checked").val()){
        $("#car").show();
        $("table td:nth-child("+(cari + 1)+")").show();
    }else{
        $("#car").hide();
        $("table td:nth-child("+(cari + 1)+")").hide();
    }

    if ($("input:checkbox[name=shape]:checked").val()){
        $("#shape").show();
        $("table td:nth-child("+(shapei + 1)+")").show();
    }else{
        $("#shape").hide();
        $("table td:nth-child("+(shapei + 1)+")").hide();
    }

    if ($("input:checkbox[name=dimensions]:checked").val()){
        $("#dimensions").show();
        $("table td:nth-child("+(dimensionsi + 1)+")").show();
    }else{
        $("#dimensions").hide();
        $("table td:nth-child("+(dimensionsi + 1)+")").hide();
    }

    if ($("input:checkbox[name=atributes]:checked").val()){
        $("#atributes").show();
        $("table td:nth-child("+(atributesi + 1)+")").show();
    }else{
        $("#atributes").hide();
        $("table td:nth-child("+(atributesi + 1)+")").hide();
    }

    if ($("input:checkbox[name=check]:checked").val()){
        $("#check").show();
        $("table td:nth-child("+(checki + 1)+")").show();
    }else{
        $("#check").hide();
        $("table td:nth-child("+(checki + 1)+")").hide();
    }

    if ($("input:checkbox[name=reference]:checked").val()){
        $("#reference").show();
        $("table td:nth-child("+(referencei + 1)+")").show();
    }else{
        $("#reference").hide();
        $("table td:nth-child("+(referencei + 1)+")").hide();
    }

    if ($("input:checkbox[name=ecode]:checked").val()){
        $("#ecode").show();
        $("table td:nth-child("+(ecodei + 1)+")").show();
    }else{
        $("#ecode").hide();
        $("table td:nth-child("+(ecodei + 1)+")").hide();
    }

    if ($("input:checkbox[name=category]:checked").val()){
        $("#category").show();
        $("table td:nth-child("+(categoryi + 1)+")").show();
    }else{
        $("#category").hide();
        $("table td:nth-child("+(categoryi + 1)+")").hide();
    }

    if ($("input:checkbox[name=vendor]:checked").val()){
        $("#vendor").show();
        $("table td:nth-child("+(vendori + 1)+")").show();
    }else{
        $("#vendor").hide();
        $("table td:nth-child("+(vendori + 1)+")").hide();
    }
});

// Activar filtros de dimension y atributos ---------------------------------------------------------------------------
const $List2 = $("#headerList2");
$("#headerList2").each(function(){
    $(this).find("input").each(function(){
        var comp = $(this).attr("name")
        $(this).prop("checked",false);
    })
})

const $List3 = $("#headerList3");
$("#headerList3").each(function(){
    $(this).find("input").each(function(){
        var comp = $(this).attr("name")
        $(this).prop("checked",false);
    })
})

const $List5 = $("#headerList5");
$("#headerList5").each(function(){
    $(this).find("input").each(function(){
        var comp = $(this).attr("name")
        $(this).prop("checked",false);
    })
})

const $List6 = $("#headerList6");
$("#headerList6").each(function(){
    $(this).find("input").each(function(){
        var comp = $(this).attr("name")
        $(this).prop("checked",false);
    })
})

$List2.change(function(){           // Activar filtro de dimensiones

    var bo = false
    // alert($(this).find("input").attr("name"))                    checkDiameter

    $(this).find("input").each(function(){
        var aux = $(this).attr("name").split("check")[1]
        // alert("Aux: "+aux)
        if ($("input:checkbox[name="+$(this).attr("name")+"]:checked").val()){
            $("#"+aux+"Filter").show();
            // alert($("#"+aux+"Min").val())
            $("#"+aux+"Min").val(1)
        }else{
            $("#"+aux+"Filter").hide();
            // alert($("#"+aux+"Filter").text())
            $("#"+aux+"Min").val(null)
            $("#"+aux+"Max").val(null)
        }
    })

    $(this).find("input").each(function(){
        var aux = $(this).attr("name").split("check")[1]
        if ($("input:checkbox[name="+$(this).attr("name")+"]:checked").val()){
            bo = true
        }
    })

    $List3.find("input").each(function(){
        var aux = $(this).attr("name").split("check")[1]
        if ($("input:checkbox[name="+$(this).attr("name")+"]:checked").val()){
            bo = true
        }
    })

    if (bo == true){
        $("#ButtonFilter").show();
    }else{
        $("#ButtonFilter").hide();
    }
})

$List3.change(function(){           // Activar filtro de atributos

    var bo = false
    var atrName = []
    var atrVal = []
    var uniqName = []
    var uniqVal = []
    var atrContent = []
    var allVal = []
    allAtr = []
    var onlyAtr = []

    $("table tr").find("td").each(function(){

        if($(this).index()==$("#atributes").index()){
            $(this).find("a").each(function(){
                // alert($(this).text())
                $(this).find("#AtrVal").each(function(){
                    // alert($(this).text())
                    allVal.push($(this).text())         // on - FOAM - off
                })

                $(this).find("#AtrName").each(function(){
                    // alert($(this).text())
                    allAtr.push($(this).text().replace(' ',''))         // Atr1 - Uno Dos
                    onlyAtr.push($(this).text().replace(' ',''))         // Atr1 - Uno Dos
                })

                atrContent.push($(this).text())
                // alert(atrContent)        // Atron - Atr2off
            })
        }
    })
    // alert(allAtr)
    // alert(atrContent)
    
    // alert(allAtr)       // El Atr,Atr,material
    // alert(allVal)    // on,off,FOAM
    for(var i = onlyAtr.length -1; i >=0; i--){
        if(onlyAtr.indexOf(onlyAtr[i]) !== i) onlyAtr.splice(i,1);
    }
    // alert(allAtr)
    // alert(onlyAtr)
    // .replace('remplazar','reemplazado')
    var atrValues = []
    var spl
    $(this).find("input").each(function(){
        var aux = $(this).attr("name").split("check")[1]        // Todos los atributos de la base
        // alert("Aux: "+aux)      // Atr - Atr2
        if ($("input:checkbox[name="+$(this).attr("name")+"]:checked").val()){
            $("#"+aux+"Filter").show();
        }else{
            $("#"+aux+"Filter").hide();
            $("#"+aux).val(null)
        }
        
    })


    for (var i=0; i<onlyAtr.length; i++){
        // alert(onlyAtr[i])
        for(var j=0;j<allAtr.length;j++){
            // alert(allAtr[j])
            if(onlyAtr[i].toLowerCase() == allAtr[j].toLowerCase()){     // Si los atributos se llaman igual
                atrValues.push(allVal[j])
            }
            
        }
        // alert(atrValues)
        // alert(atrValues.length)
        for(var k = atrValues.length -1; k >=0; k--){
            if(atrValues.indexOf(atrValues[k]) !== k)
                atrValues.splice(k,1);
        }
        $("#"+onlyAtr[i]+"Filter button").attr("data-bs-content",atrValues)
        atrValues = []
    }

    $(this).find("input").each(function(){
        var aux = $(this).attr("name").split("check")[1]
        if ($("input:checkbox[name="+$(this).attr("name")+"]:checked").val()){
            bo = true
        }
    })

    $List2.find("input").each(function(){
        var aux = $(this).attr("name").split("check")[1]
        if ($("input:checkbox[name="+$(this).attr("name")+"]:checked").val()){
            bo = true
        }
    })

    if (bo === true){
        $("#ButtonFilter").show();
    }else{
        $("#ButtonFilter").hide();
    }
})
// compCategories = []                 // Lista de categorias seleccionadas
$List5.change(function(){           // Activar filtro de Categories
    contTotalTable = []
    // alert("compVendors: "+compVendors)
    for(var i = listadoPasar.length -1; i >=0; i--){
        if(listadoPasar.indexOf(listadoPasar[i]) !== i) listadoPasar.splice(i,1);
    }
    compCategories = []
    contCategory = []

    var catVal = []
    prueba = 5
    var trnum = 0
    // Guarda la cantidad de filas seleccionadas
    var maxRows = parseInt($("#maxRows").val())
    var semiTotalRows = $(table+" tbody tr").length
    totalRows = listadoPasar.length
    var rev = false
    var is = false
    var listCont = 0
    var aCont = 0

    $("tbody tr").each(function(){
        $(this).hide()
    })

    $("table td a").each(function(){
        if ($(this).attr("id") == "categoryInfo"){
            catVal.push($(this).text())
        }
    })
    for(var i = catVal.length -1; i >=0; i--){
        if(catVal.indexOf(catVal[i]) !== i) catVal.splice(i,1);
    }
    // var tamCat = []
    var cont = 0
    inputTotal = 0
    // Cuento los checks activos de Categoria
    $(this).find("input").each(function(){  // compCategories son todos los check activos
        inputTotal = inputTotal + 1
        var aux = $(this).attr("name").split("check")[1]        // Todos los atributos de la base
        if ($("input:checkbox[name="+$(this).attr("name")+"]:checked").val()){
            comp = $(this).attr("name").split("check")[1]
            compCategories.push(comp)

        }
        else{
            cont = cont +1
        }
    })
    // Aqui empieza el filtro ---------------------------------------------------
    var contAtrFind = 0
    $("tbody tr").each(function(){      // Recorro por filas
        // alert($(this).text())
        trnum++//paginado
        var bandShow = false
        var bandShow2 = false
        $(this).find("a").each(function(){      // Recorro por a

            if(compCategories.length>0){
                if ($(this).attr("id") == "categoryInfo"){      // Si la columna es Category
                    for(var k=0;k<compCategories.length;k++){ 
                        // if((compCategories[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
                        if(compCategories[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
                            bandShow = true
                            contCategory.push($(this).text())
                        }
                    }
                }
            }

            if(listadoPasar.length>0){  // Si se trae valores de Dimension o atributos
                if($(this).parent().parent().index()==$("#dimensions").index() || $(this).parent().parent().index()==$("#atributes").index()){
                    for(var i=0; i<listadoPasar.length; i++){
                        if((listadoPasar[i].replace(' ','').toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
                            contAtrFind = contAtrFind + 1
                            bandDimAtr = true
                        }
                    }
                }
            }
            if ($(this).attr("id") == "vendorInfo"){      // Si la columna es Vendor
                for(var k=0;k<compVendors.length;k++){ 
                    if(compVendors[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
                        bandShow2 = true
                        // contVendor.push($(this).text())
                    }
                }
            }






            // if ($(this).attr("id") == "categoryInfo"){      // Si la columna es Category
            //     for(var k=0;k<compCategories.length;k++){ 
            //         // if((compCategories[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
            //         if(compCategories[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
            //             bandShow = true
            //             contCategory.push($(this).text())
            //         }
            //     }
            // }

            // if(listadoPasar.length>0){  // Si se trae velores de Dimension o atributos
            //     if($(this).parent().parent().index()==$("#dimensions").index() || $(this).parent().parent().index()==$("#atributes").index()){
            //         for(var i=0; i<listadoPasar.length; i++){
            //             if((listadoPasar[i].replace(' ','').toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
            //                 if(bandShow == true){
            //                     // listCont++ //paginado
            //                     // $(this).parent().parent().parent().show()
            //                     contAtrFind = contAtrFind + 1
            //                     is = true // inventado de paginado
            //                 }
            //                 else{
            //                     is = false //paginado
            //                 }
            //             }
            //             // else{
            //             //     contAtrFind = contAtrFind + 1
            //             // }
            //         }
            //     }

            // }
            // // alert("compVendors: "+compVendors)
            // if(compVendors.length>0){
            //     if ($(this).attr("id") == "vendorInfo"){      // Si la columna es Category
            //         for(var k=0;k<compVendors.length;k++){ 
            //             // if((compCategories[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
            //             if(compVendors[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
            //                 bandShow2 = true
            //                 // contCategory.push($(this).text())
            //             }
            //         }
            //     }
            // }
            // if((bandShow == true) || (bandShow2 == true)){
            //     is = true
            // }
            
        }) // termina a
        if(listadoPasar.length>0){ // Si trae filtro de dimensiones y atributos

            if(compVendors.length>0){
                if ((listadoAll == contAtrFind) && (bandShow == true && bandShow2 == true)){
                    is = true
                    contTotalTable.push($(this).text())
                }
                else{
                    is = false
                }
            }
            else{
                if ((listadoAll == contAtrFind) && (bandShow == true)){
                    is = true
                    contTotalTable.push($(this).text())
                }
                else{
                    is = false
                }
            }
            
            if(is == true){
                rev = true
                if(trnum > maxRows){
                    $(this).hide()
                }
                if(trnum <= maxRows){
                    $(this).show()
                }
            }
            if(rev===false){
                trnum--
            }else{
                rev = false
            }
            is = true


            // if(compVendors.length>0){
            //     if ((listadoAll == contAtrFind) && (bandShow == true && bandShow2 == true)){
            //         is = true
            //         contTotalTable.push($(this).text())
            //     }
            //     else{
            //         is = false
            //     }
            // }
            // else{
            //     if ((listadoAll == contAtrFind) && (bandShow == true)){
            //         is = true
            //         contTotalTable.push($(this).text())
            //     }
            //     else{
            //         is = false
            //     }
            // }
            
            // if(is == true){
            //     rev = true
            //     if(trnum > maxRows){
            //         $(this).hide()
            //     }
            //     if(trnum <= maxRows){
            //         $(this).show()
            //     }
            // }
            // if(rev===false){
            //     trnum--
            // }else{
            //     rev = false
            // }
            // is = true
        }
        else{  // Muestro cuando no trae filtro de dimensiones ni atributos
            // alert($(this).text())
            // alert("bandShow: "+bandShow+" bandShow2: "+bandShow2)
            // alert("compCategories: "+compCategories+" compVendors: "+compVendors)
            if(compCategories.length>0 && compVendors.length>0){
                if((bandShow == true) && (bandShow2 == true)){
                    is = true
                    // alert("Muestro: "+$(this).text())
                    contTotalTable.push($(this).text())
                }
                else{
                    is = false
                }
            }
            else{
                if(compVendors.length<1){
                    if(bandShow == true){
                        is = true
                        contTotalTable.push($(this).text())
                        // alert("Tambien: "+$(this).text())
                    }
                    else{
                        is = false
                    }
                }
            }
            // alert("is: "+is)
            // alert("trnum: "+trnum+" maxRows: "+maxRows)
            if(is == true){
                rev = true
                if(trnum > maxRows){
                    $(this).hide()
                }
                if(trnum <= maxRows){
                    $(this).show()
                }
            }
            if(rev===false){
                trnum--
            }else{
                rev = false
            }
            is = true
            // contAtrFind = 0
        }

        contAtrFind = 0

        // if(listadoPasar.length>0){ // Si trae filtro de dimensiones y atributos
        //     // if ((listadoAll == contAtrFind) && bandShow == true){
        //     if ((listadoAll == contAtrFind)){
        //         is = true
        //         listadoCategory.push($(this).text())
        //     }
        //     else{ // desde aqui es paginacion
        //         is = false
        //     }if(is == true){
        //         rev = true
        //         if(trnum > maxRows){
        //             $(this).hide()
        //         }
        //         if(trnum <= maxRows){
        //             $(this).show()
        //         }
        //     }
        //     if(rev===false){
        //         trnum--
        //     }else{
        //         rev = false
        //     }
        //     is = true // hasta aqui
        //     // else{
        //     //     is = false
        //     // }
        // }
        // else{  // Muestro cuando no trae filtro de dimensiones ni atributos
        //     // alert("band1 y band2: "+bandShow+" "+bandShow2)
        //     if((bandShow == true) || (bandShow2 == true)){
        //         is = true
        //         // alert("is True")
        //     }
        //     else{
        //         is = false
        //     }
        //     if(is == true){
        //         rev = true
        //         if(trnum > maxRows){
        //             $(this).hide()
        //         }
        //         if(trnum <= maxRows){
        //             $(this).show()
        //         }
        //     }
        //     if(rev===false){
        //         trnum--
        //     }else{
        //         rev = false
        //     }
        //     is = true
        //     // contAtrFind = 0
        // }

        // contAtrFind = 0
    }) // fin del tr
    // alert(contTotalTable)
    // alert(contTotalTable.length)
    // alert("Ahora si")
    // Si checkbox está vacío ------------------------------------------------------
    if (inputTotal == cont){        // Si el checkbox está vacío    
        if(listadoPasar.length>0){      // Si se ha filtrado antes por dimension o atributos
            trnum = 0
            $("tbody tr").each(function(){
                trnum++
                contAtrFind = 0
                $($(this).find("a")).each(function(){
                    if($(this).parent().parent().index()==$("#dimensions").index() || $(this).parent().parent().index()==$("#atributes").index()){
                        for(var i=0; i<listadoPasar.length; i++){
                            if((listadoPasar[i].replace(' ','').toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
                                // $(this).parent().parent().parent().show()
                                // listadoCategory.push($(this).parent().parent().text())
                                contAtrFind = contAtrFind + 1
                                is = true
                            }
                        }
                    }
                })
                if (listadoAll == contAtrFind){
                    is = true
                    listadoCategory.push($(this).text())
                }
                else{ // desde aqui es paginacion
                    is = false
                }
                if(is == true){
                    rev = true
                    if(trnum > maxRows){
                        $(this).hide()
                    }
                    if(trnum <= maxRows){
                        $(this).show()
                    }
                }
                if(rev===false){
                    trnum--
                }else{
                    rev = false
                }
                is = true // hasta aqui
                // contAtrFind = 0
            })
        }
        else{           // Si no se ha filtrado por atributos o dimensiones

            trnum = 0
            $("tbody tr").each(function(){
                trnum++
                var bandShow = false
                $(this).find("a").each(function(){      // Recorro por a
                    if(compVendors.length>0){    // Si hay Vendors
                        if ($(this).attr("id") == "vendorInfo"){
                            for(var k=0;k<compVendors.length;k++){
                                if(compVendors[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
                                    bandShow = true
                                    contVendor.push($(this).text())
                                }
                            }
                        }
                    }
                    else{   // Si no hay Vendors
                        if ($(this).attr("id") == "categoryInfo"){
                            bandShow = true
                            contCategory.push($(this).text())
                        }
                    }
                    
                })
                if(bandShow == true){
                    // alert($(this).text())
                    is = true
                }else{
                    is = false
                }
                // alert("is: "+is+"trnum: "+trnum+"maxRows: "+maxRows)
                if(is == true){
                    rev = true
                    if(trnum > maxRows){
                        $(this).hide()
                    }
                    if(trnum <= maxRows){
                        $(this).show()
                    }
                }
                else{
                    $(this).hide()
                }
                if(rev===false){
                    trnum--
                }else{
                    rev = false
                }
                is = true
                contAtrFind = 0
            })


            // $("tbody tr").each(function(){
            //     trnum++
            //     var bandShow = false
                
            //     $(this).find("a").each(function(){      // Recorro por a
            //         if ($(this).attr("id") == "categoryInfo"){      // Si la columna es Category
            //             // contCategory.push($(this).text())
            //             bandShow = true
            //         }
            //         if(bandShow == true){
            //             is = true
            //         }
            //     })
            //     if(is == true){
            //         rev = true
            //         if(trnum > maxRows){
            //             $(this).hide()
            //         }
            //         if(trnum <= maxRows){
            //             $(this).show()
            //         }
            //     }
            //     if(rev===false){
            //         trnum--
            //     }else{
            //         rev = false
            //     }
            //     is = true
            //     contAtrFind = 0
            // })
        }
    }
    // alert(listadoCategory)
    $(".pagination").html("")
    // alert(contTotalTable)
    // alert("contTotalTable.lenth: "+contTotalTable.length)
    alert(contTotalTable)
    alert(contTotalTable.length)
    alert(contCategory)
    alert(contCategory.length)
    if(contTotalTable.length>0){
        totalRows = contTotalTable.length
    }
    else{
        totalRows = contCategory.length
    }
    alert("totalRows: "+totalRows+" maxRows: "+maxRows)
    // totalRows = contTotalTable.length
    if(totalRows > maxRows){    // Mostrar paginación
        var pagenum = Math.ceil(totalRows/maxRows)
        for(var i=1;i<=pagenum;){
            $(".pagination").append('<li class="page-item" data-page="'+i+'"><a class="page-link" href="#"><span>'+ i++ +'<span class="sr-only">(current)</span></span></a></li>').show()
        }
    }



    // // if(listadoCategory.length>0){   // Si se trae algo de Dimensiones o Atributos
    // if(listadoPasar.length>0){   // Si se trae algo de Dimensiones o Atributos
    //     totalRows = listadoCategory.length
    // }
    // else{
    //     totalRows = contCategory.length
    // }

    // // alert("totalRows: "+totalRows+" maxRows: "+maxRows)
    // if(totalRows > maxRows){    // Mostrar paginación
    //     var pagenum = Math.ceil(totalRows/maxRows)
    //     for(var i=1;i<=pagenum;){
    //         $(".pagination").append('<li class="page-item" data-page="'+i+'"><a class="page-link" href="#"><span>'+ i++ +'<span class="sr-only">(current)</span></span></a></li>').show()
    //     }
    // }
    $(".pagination li:first-child").addClass("active")
    for(var i = contCategory.length -1; i >=0; i--){
        if(contCategory.indexOf(contCategory[i]) !== i) contCategory.splice(i,1);
    }
    // alert(contCategory)


    $(".pagination li").on("click",function(){ // Cuando clickeo la numeración
        var pageNum = $(this).attr("data-page")
        var trIndex = 0;
        var rev = false
        $(".pagination li").removeClass("active")
        $(this).addClass("active")
        $(table+" tr:gt(0)").each(function(){
            trIndex++
            if(listadoPasar.length>0){  // Si trae desde atributos y dimensiones
                for(var i=0; i<contCategory.length; i++){
                    $(this).find("a").each(function(){
                        if($(this).text()==contCategory[i]){
                            rev = true
                        }
                    })
                }

                for(var i=0; i<listadoPasar.length; i++){
                    $(this).find("a").each(function(){
                        if($(this).text()==listadoPasar[i]){
                            rev = true
                            if(trIndex > (maxRows*pageNum) || trIndex <= ((maxRows*pageNum)-maxRows)){
                                $(this).parent().parent().parent().hide()
                            }else{
                                if(rev == true){
                                    $(this).parent().parent().parent().show()
                                }
                            }
                        }
                    })
                }
            }
            else{   // Si no trae nada desde atributos y dimensiones
                // alert($(this).text())
                var band1 = false
                var band2 = false
                for(var i=0; i<contCategory.length; i++){
                    $(this).find("a").each(function(){
                        if ($(this).attr("id") == "categoryInfo"){  // Si la columna es Category
                            if($(this).text()==contCategory[i]){
                                // alert("Consigue: "+$(this).text())
                                rev = true
                                band1 = true
                            }
                        }
                    })
                }
                // alert("Sale")
                // alert(contVendor)
                // MAS ADELANTE SI HAY QUE PONERLO
                if(contVendor.length>0){
                    for(var i=0; i<contVendor.length; i++){
                        $(this).find("a").each(function(){
                            if ($(this).attr("id") == "vendorInfo"){  // Si la columna es Vendor
                                if($(this).text()==contVendor[i]){
                                    rev = true
                                    band2 = true
                                }
                            }
                        })
                    }
                }
                // alert("pasa")

                if(trIndex > (maxRows*pageNum) || trIndex <= ((maxRows*pageNum)-maxRows)){
                    $(this).hide()
                }else{
                    if((band1 == true) || (band2 == true)){
                        $(this).show()
                    }
                }
            }
            if(rev===false){
                trIndex--
            }else{
                rev = false
            }
        })
    })
    // listadoAll = inputTotal-cont
    for(var x = 0;x < listadoCategory.length; x++){
        pasarCategory.push(listadoCategory[x])
    }
    listadoCategory = []


    // $(".pagination li").on("click",function(){ // Cuando clickeo la numeración
    //     var pageNum = $(this).attr("data-page")
    //     var trIndex = 0;
    //     var rev = false
    //     $(".pagination li").removeClass("active")
    //     $(this).addClass("active")
    //     $(table+" tr:gt(0)").each(function(){
    //         trIndex++
    //         if(listadoPasar.length>0){  // Si trae desde atributos y dimensiones
    //             for(var i=0; i<contCategory.length; i++){
    //                 $(this).find("a").each(function(){
    //                     if($(this).text()==contCategory[i]){
    //                         rev = true
    //                     }
    //                 })
    //             }

    //             for(var i=0; i<listadoPasar.length; i++){
    //                 $(this).find("a").each(function(){
    //                     if($(this).text()==listadoPasar[i]){
    //                         rev = true
    //                         if(trIndex > (maxRows*pageNum) || trIndex <= ((maxRows*pageNum)-maxRows)){
    //                             $(this).parent().parent().parent().hide()
    //                         }else{
    //                             if(rev == true){
    //                                 $(this).parent().parent().parent().show()
    //                             }
    //                         }
    //                     }
    //                 })
    //             }
    //         }
    //         else{   // Si no trae nada desde atributos y dimensiones
    //             // alert(contCategory)
    //             // alert(contCategory.length)
    //             for(var i=0; i<contCategory.length; i++){
    //                 $(this).find("a").each(function(){
    //                     if($(this).text()==contCategory[i]){
    //                         rev = true
    //                         if(trIndex > (maxRows*pageNum) || trIndex <= ((maxRows*pageNum)-maxRows)){
    //                             $(this).parent().parent().hide()
    //                         }else{
    //                             $(this).parent().parent().show()
    //                         }
    //                     }
    //                 })
    //             }
    //         }

    //         if(rev===false){
    //             trIndex--
    //         }else{
    //             rev = false
    //         }
    //     })
    // })
    // // listadoAll = inputTotal-cont
    // for(var x = 0;x < listadoCategory.length; x++){
    //     pasarCategory.push(listadoCategory[x])
    // }
    // listadoCategory = []
})























$List6.change(function(){           // Activar filtro de Vendors
    for(var i = listadoPasar.length -1; i >=0; i--){
        if(listadoPasar.indexOf(listadoPasar[i]) !== i) listadoPasar.splice(i,1);
    }
    compVendors = []
    contVendor = []
    contTotalTable = []

    var catVal = []
    prueba = 5
    var trnum = 0
    // Guarda la cantidad de filas seleccionadas
    var maxRows = parseInt($("#maxRows").val())
    var semiTotalRows = $(table+" tbody tr").length
    totalRows = listadoPasar.length
    var rev = false
    var is = false
    var listCont = 0
    var aCont = 0

    $("tbody tr").each(function(){
        $(this).hide()
    })
    $("table td a").each(function(){
        if ($(this).attr("id") == "vendorInfo"){
            catVal.push($(this).text())
        }
    })
    for(var i = catVal.length -1; i >=0; i--){
        if(catVal.indexOf(catVal[i]) !== i) catVal.splice(i,1);
    }
    var cont = 0
    inputTotal = 0
    // Cuento los checks activos de Vendor -------------------------------------
    $(this).find("input").each(function(){  // compCategories son todos los check activos
        inputTotal = inputTotal + 1
        var aux = $(this).attr("name").split("check")[1]        // Todos los vendors de la base
        if ($("input:checkbox[name="+$(this).attr("name")+"]:checked").val()){
            comp = $(this).attr("name").split("check")[1]
            compVendors.push(comp)
        }
        else{
            cont = cont +1
        }
    })
    // Aqui empieza el filtro ---------------------------------------------------
    var contAtrFind = 0
    $("tbody tr").each(function(){      // Recorro por filas
        trnum++//paginado
        var bandShow = false
        var bandShow2 = false
        var bandDimAtr = false
        $(this).find("a").each(function(){      // Recorro por a

            if(compCategories.length>0){
                if ($(this).attr("id") == "categoryInfo"){      // Si la columna es Category
                    for(var k=0;k<compCategories.length;k++){ 
                        // if((compCategories[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
                        if(compCategories[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
                            bandShow2 = true
                            // contCategory.push($(this).text())
                        }
                    }
                }
            }

            if(listadoPasar.length>0){  // Si se trae valores de Dimension o atributos
                if($(this).parent().parent().index()==$("#dimensions").index() || $(this).parent().parent().index()==$("#atributes").index()){
                    for(var i=0; i<listadoPasar.length; i++){
                        if((listadoPasar[i].replace(' ','').toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
                            contAtrFind = contAtrFind + 1
                            bandDimAtr = true
                        }
                    }
                }
            }
            if ($(this).attr("id") == "vendorInfo"){      // Si la columna es Vendor
                for(var k=0;k<compVendors.length;k++){ 
                    if(compVendors[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
                        bandShow = true
                        contVendor.push($(this).text())
                    }
                }
            }

        })  // Fin de a
        if(listadoPasar.length>0){ // Si trae filtro de dimensiones y atributos

            if(compCategories.length>0){
                if ((listadoAll == contAtrFind) && (bandShow == true && bandShow2 == true)){
                    is = true
                    contTotalTable.push($(this).text())
                }
                else{
                    is = false
                }
            }
            else{
                if ((listadoAll == contAtrFind) && (bandShow == true)){
                    is = true
                    contTotalTable.push($(this).text())
                }
                else{
                    is = false
                }
            }
            
            if(is == true){
                rev = true
                if(trnum > maxRows){
                    $(this).hide()
                }
                if(trnum <= maxRows){
                    $(this).show()
                }
            }
            if(rev===false){
                trnum--
            }else{
                rev = false
            }
            is = true
        }
        else{  // Muestro cuando no trae filtro de dimensiones ni atributos
            if(compCategories.length>0 && compVendors.length>0){
                if((bandShow == true) && (bandShow2 == true)){
                    is = true
                    contTotalTable.push($(this).text())
                }
                else{
                    is = false
                }
            }
            else{
                if(compCategories.length<1){
                    if(bandShow == true){
                        is = true
                        contTotalTable.push($(this).text())
                    }
                    else{
                        is = false
                    }
                }
            }
            if(is == true){
                rev = true
                if(trnum > maxRows){
                    $(this).hide()
                }
                if(trnum <= maxRows){
                    $(this).show()
                }
            }
            if(rev===false){
                trnum--
            }else{
                rev = false
            }
            is = true
            // contAtrFind = 0
        }

        contAtrFind = 0
    }) // fin del tr

    // Si checkbox está vacío ------------------------------------------------------
    if (inputTotal == cont){        // Si el checkbox está vacío    
        if(listadoPasar.length>0){      // Si se ha filtrado antes por dimension o atributos
            trnum = 0
            is = false
            $("tbody tr").each(function(){
                bandShow2 = false
                trnum++
                contAtrFind = 0
                $($(this).find("a")).each(function(){

                    if($(this).parent().parent().index()==$("#dimensions").index() || $(this).parent().parent().index()==$("#atributes").index()){
                        for(var i=0; i<listadoPasar.length; i++){
                            if((listadoPasar[i].replace(' ','').toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
                                // listadoCategory.push($(this).parent().parent().text())
                                contAtrFind = contAtrFind + 1
                            }
                        }
                    }

                    if(compCategories.length>0){
                        if ($(this).attr("id") == "categoryInfo"){      // Si la columna es Category
                            for(var k=0;k<compCategories.length;k++){ 
                                // if((compCategories[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
                                if(compCategories[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
                                    bandShow2 = true
                                    // contCategory.push($(this).text())
                                }
                            }
                        }
                    }
                })
                if(compCategories.length>0){
                    if ((listadoAll == contAtrFind) && (bandShow2 == true)){
                        is = true
                        contTotalTable.push($(this).text())
                        listadoCategory.push($(this).text())
                    }
                    else{ // desde aqui es paginacion
                        is = false
                    }
                }
                else{
                    if ((listadoAll == contAtrFind)){
                        is = true
                        contTotalTable.push($(this).text())
                        listadoCategory.push($(this).text())
                    }
                    else{ // desde aqui es paginacion
                        is = false
                    }
                }
                
                if(is == true){
                    rev = true
                    if(trnum > maxRows){
                        $(this).hide()
                    }
                    if(trnum <= maxRows){
                        $(this).show()
                    }
                }
                if(rev===false){
                    trnum--
                }else{
                    rev = false
                }
                is = true // hasta aqui
            })
        }
        else{           // Si no se ha filtrado por atributos o dimensiones
            var contTotal = 0
            trnum = 0
            $("tbody tr").each(function(){
                trnum++
                var bandShow = false
                $(this).find("a").each(function(){      // Recorro por a
                    if(compCategories.length>0){    // Si hay categorias
                        if ($(this).attr("id") == "categoryInfo"){
                            for(var k=0;k<compCategories.length;k++){
                                if(compCategories[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
                                    bandShow = true
                                    contCategory.push($(this).text())
                                }
                            }
                        }
                    }
                    else{   // Si no hay categorias
                        if ($(this).attr("id") == "vendorInfo"){
                            bandShow = true
                            contVendor.push($(this).text())
                        }
                    }
                    
                })
                if(bandShow == true){
                    is = true
                }else{
                    is = false
                }
                if(is == true){
                    rev = true
                    if(trnum > maxRows){
                        $(this).hide()
                    }
                    if(trnum <= maxRows){
                        $(this).show()
                    }
                }
                else{
                    $(this).hide()
                }
                if(rev===false){
                    trnum--
                }else{
                    rev = false
                }
                is = true
                contAtrFind = 0
            })
        }
    }
    $(".pagination").html("")
    if(contTotalTable.length>0){
        totalRows = contTotalTable.length
    }
    else{
        totalRows = contVendor.length
    }
    // totalRows = contTotalTable.length
    if(totalRows > maxRows){    // Mostrar paginación
        var pagenum = Math.ceil(totalRows/maxRows)
        for(var i=1;i<=pagenum;){
            $(".pagination").append('<li class="page-item" data-page="'+i+'"><a class="page-link" href="#"><span>'+ i++ +'<span class="sr-only">(current)</span></span></a></li>').show()
        }
    }
    $(".pagination li:first-child").addClass("active")
    // for(var i = contVendor.length -1; i >=0; i--){
    //     if(contVendor.indexOf(contVendor[i]) !== i) contVendor.splice(i,1);
    // }
    $(".pagination li").on("click",function(){ // Cuando clickeo la numeración
        var pageNum = $(this).attr("data-page")
        var trIndex = 0;
        var rev = false
        $(".pagination li").removeClass("active")
        $(this).addClass("active")
        $(table+" tr:gt(0)").each(function(){
            trIndex++
            if(listadoPasar.length>0){  // Si trae desde atributos y dimensiones
                for(var i=0; i<contCategory.length; i++){
                    $(this).find("a").each(function(){
                        if($(this).text()==contCategory[i]){
                            rev = true
                        }
                    })
                }

                for(var i=0; i<listadoPasar.length; i++){
                    $(this).find("a").each(function(){
                        if($(this).text()==listadoPasar[i]){
                            rev = true
                            if(trIndex > (maxRows*pageNum) || trIndex <= ((maxRows*pageNum)-maxRows)){
                                $(this).parent().parent().parent().hide()
                            }else{
                                if(rev == true){
                                    $(this).parent().parent().parent().show()
                                }
                            }
                        }
                    })
                }
            }
            else{   // Si no trae nada desde atributos y dimensiones
                var band1 = false
                var band2 = false
                for(var i=0; i<contVendor.length; i++){
                    $(this).find("a").each(function(){
                        if ($(this).attr("id") == "vendorInfo"){  // Si la columna es Vendor
                            if($(this).text()==contVendor[i]){
                                rev = true
                                band1 = true
                            }
                        }
                    })
                }
                if(contCategory.length>0){
                    for(var i=0; i<contCategory.length; i++){
                        $(this).find("a").each(function(){
                            if ($(this).attr("id") == "categoryInfo"){  // Si la columna es Category
                                if($(this).text()==contCategory[i]){
                                    rev = true
                                    band2 = true
                                }
                            }
                        })
                    }
                }
                if(trIndex > (maxRows*pageNum) || trIndex <= ((maxRows*pageNum)-maxRows)){
                    $(this).hide()
                }else{
                    if((band1 == true) || (band2 == true)){
                        $(this).show()
                    }
                }
            }
            if(rev===false){
                trIndex--
            }else{
                rev = false
            }
        })
    })
    // listadoAll = inputTotal-cont
    for(var x = 0;x < listadoCategory.length; x++){
        pasarCategory.push(listadoCategory[x])
    }
    listadoCategory = []

})

// Arreglar por click a cabecera ----------------------------------------------------------------------------------
// Se debe agregar CSS th { cursor: pointer; }
$('th').not("#check").click(function(){
    var table = $(this).parents('table').eq(0)
    var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()))
    this.asc = !this.asc
    if (!this.asc){rows = rows.reverse()}
    for (var i = 0; i < rows.length; i++){table.append(rows[i])}

    var i = 1;
    $("tbody tr").each(function(){
        $(this).find("td").each(function(){
            if($(this).index()==$("#detail-id").index()){
                if($(this).parent().is(":visible")){
                    $(this).text(i)
                    i=i+1;
                }
            }
            
        })
    });

})
function comparer(index) {
    return function(a, b) {
        var valA = getCellValue(a, index), valB = getCellValue(b, index)
        return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB)
    }
}
function getCellValue(row, index){ return $(row).children('td').eq(index).text() }

// Enumerar tabla de carrito --------------------------------------------------------------------------------------

var i = 1;
$("tbody tr").each(function(){
    $(this).find("td").each(function(){
        if($(this).index()==$("#detail-id").index()){
            $(this).text(i);
            i=i+1;
        }
        
    })
});

// Agrandar la foto al clickearla ---------------------------------------------------------------
$(".photo").click(function(a){

    var bo = false;

    var newCss = {
        "background-size": "200px 200px",
        "width": "200px",
        "height": "200px"
    }
    var oldCss = {
        "background-size": "80px 80px",
        "width": "80px",
        "height": "80px"
    }

    if($(this).css("width")==="200px"){
        bo = true;
        $(this).css(oldCss);
    }

    $("#myTable tr").each(function(){
            $(this).find(".photo").each(function(){
                $(this).css(oldCss);
            })
    })

    if(bo === true){
        $(this).css(oldCss);
    }else{
        $(this).css(newCss);
    }
    a.preventDefault()
})

// Paginacion -------------------------------------------------------------------------------------

$("#maxRows").on("change",function(){
    var listadoTotal = 0
    var listadoTam = 0
    if (listado.length > 0){        // Si tiene algo desde Atributos o Dimensiones
        $(".pagination").html("")
        var trnum = 0
        var maxRows = parseInt($("#maxRows").val())
        var semiTotalRows = $(table+" tbody tr").length
        var rev = false
        $(table+' tr:gt(0)').each(function(){
            var contCons = 0
            is = false
            trnum++
            $(this).find("a").each(function(){
                for(var i=0; i<listado.length; i++){

                    if($(this).text()===listado[i]){
                        is = true
                        listadoTam++
                        // rev=true
                        // alert("Consigue: "+$(this).text())
                        // rev = true
                        // alert("trnum: "+trnum+" maxRows: "+maxRows)
                        // if(trnum > maxRows){
                        //     alert("Hide")
                        //     $(this).parent().parent().parent().hide()
                        // }
                        // if(trnum <= maxRows){
                        //     alert("Show")
                        //     $(this).parent().parent().parent().show()
                        //     listadoTam++
                        // }
                    }
                }
            })
            
            // if(listado.length == listadoTam){
            if(listadoAll == listadoTam){
                listadoTotal++
                is = true
            }else{
                is = false
            }
            if(is == true){
                rev = true
                if(trnum > maxRows){
                    $(this).hide()
                }
                if(trnum <= maxRows){
                    $(this).show()
                }
            }
            if(rev===false){
                trnum--
            }else{
                rev = false
            }
            is = true
            listadoTam = 0
        })
        totalRows = listadoTotal
        if(totalRows > maxRows){
            var pagenum = Math.ceil(totalRows/maxRows)
            for(var i=1;i<=pagenum;){
                $(".pagination").append('<li class="page-item" data-page="'+i+'"><a class="page-link" href="#"><span>'+ i++ +'<span class="sr-only">(current)</span></span></a></li>').show()
            }
        }
        $(".pagination li:first-child").addClass("active")
        $(".pagination li").on("click",function(){
            var pageNum = $(this).attr("data-page")
            var trIndex = 0;
            var rev = false
            $(".pagination li").removeClass("active")
            $(this).addClass("active")
            listadoTam = 0
            listadoTotal = 0

            
            $(table+" tr:gt(0)").each(function(){
                // is = false
                trIndex++
                for(var i=0; i<listadoPasar.length; i++){
                    $(this).find("a").each(function(){
                        if($(this).text()==listadoPasar[i]){
                            rev = true
                            if(trIndex > (maxRows*pageNum) || trIndex <= ((maxRows*pageNum)-maxRows)){
                                $(this).parent().parent().parent().hide()
                            }else{
                                if(rev == true){
                                    $(this).parent().parent().parent().show()
                                }
                            }
                        }
                    })
                }

                if(rev===false){
                    trIndex--
                }else{
                    rev = false
                }

                // contAtrFind = 0

            })
        })
    }else{      // Si no tiene nada desde atributos o dimensiones
        // alert("Entra")
        $(".pagination").html("")
        var trnum = 0
        // var totalRows = 0
        // Guarda la cantidad de filas seleccionadas
        var maxRows = parseInt($(this).val())
        // $("#myTable tr").each(function(){
        //     if($(this).is(":visible")){
        //         totalRows++
        //     }
        // })
        // alert(totalRows)
        var totalRows = $(table+" tbody tr").length
        $(table+' tr:gt(0)').each(function(){
            trnum++
            if(trnum > maxRows){
                $(this).hide()
            }
            if(trnum <= maxRows){
                $(this).show()
            }
            // if($(this).is(":visible")===false){
            //     $(this).hide()
            // }else{
            //     $(this).show()
            // }
        })
        if(totalRows > maxRows){
            // Guardo la cantidad de paginas que se necesitan
            var pagenum = Math.ceil(totalRows/maxRows)
            for(var i=1;i<=pagenum;){
                $(".pagination").append('<li class="page-item" data-page="'+i+'"><a class="page-link" href="#"><span>'+ i++ +'<span class="sr-only">(current)</span></span></a></li>').show()
            }
        }
        $(".pagination li:first-child").addClass("active")
        $(".pagination li").on("click",function(){
            var pageNum = $(this).attr("data-page")
            var trIndex = 0;
            $(".pagination li").removeClass("active")
            $(this).addClass("active")
            // Recorre tolas las filas de la tabla
            $(table+" tr:gt(0)").each(function(){
                trIndex++
                if(trIndex > (maxRows*pageNum) || trIndex <= ((maxRows*pageNum)-maxRows)){
                    $(this).hide()
                }else{
                    $(this).show()
                }
            })
        })
    }
})

$(document).ready(function(){
    $('[data-toggle="popover"]').popover()
 })

 // Para mostrar solo 5 codigos de referencia por Spare
//  "#myTable tr"
 $("table").find("tr").each(function(){
cont = 0
    $(this).find("td").each(function(){

        // if($(this).attr("id")=="reference"){
        if($(this).index()==$("#reference").index()){
            $(this).find("div").each(function(){
                // alert($(this).text())
                // alert(cont)
                if(cont<5){
                    $(this).show()
                }else{
                    $(this).hide()
                }
                cont = cont +1
            })
        }
    })
     
 })

 $("table").find("tr").each(function(){
    cont = 0
        $(this).find("td").each(function(){
    
            // if($(this).attr("id")=="reference"){
            if($(this).index()==$("#atributes").index()){
                // alert($(this).text())
                $(this).find("a").each(function(){
                    // alert($(this).text())
                    var aux = $(this).text()
                    var sp = aux.split(" ")
                    var der = sp[sp.length-1]
                    // alert(der)
                    var iz = aux.split(" "+der)
                    iz = iz[0]
                    // alert(iz)
                    // iz.attr("style",'background-color:gray')
                    // iz.css({'background-color':'gray'})
                    // $(this).text(iz+" Valor")
                    // alert($(this).text())
                    // alert(cont)
                    // if(cont<5){
                    //     $(this).show()
                    // }else{
                    //     $(this).hide()
                    // }
                    // cont = cont +1
                })
            }
        })
         
     })