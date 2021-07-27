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
var contCategory = []
var pasarCategory = []


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
            // alert("innerAtribute: "+innerAtribute)
            if(!($(this).attr("id").split("Min")[1]=="" || $(this).attr("id").split("Max")[1]=="")){
                AtributeString = comp                       // on - off
                // alert("AtributeString: "+AtributeString)
                if(AtributeString!=""){
                    listadoAll++
                }
            }
            if(dimAtribute === innerAtribute){
                // alert("dimAtribute: "+dimAtribute)
                // alert("comp: "+comp)
                AtributeMin = comp
            }else{
                AtributeMax = comp
            }
        })

        // $(this).find()

        // $(".cantainer").each(function(){
        //     alert($(this).text())
        //     $(this).find("div").each(function(){
        //         // alert($(this).text())
        //     })
        // })

        $('#myTable tr a').each(function(){
            if($(this).attr("id")===(dimAtribute+"Value")){
                $(this).find(".cantainer").each(function(){
                    // alert($(this).text())
                    // alert($(this).find("#AtrName").text())
                    var varSplit = $(this).find("#AtrName").text()
                    var valor = $(this).find("#AtrVal").text()      // 88.0 mm - on - FOAM
                    // alert(valor)
                    aux = valor.split(" mm")
                    // alert(aux)
                    // alert(aux.length)
                    if(aux.length>1){
                        var VarFloat = parseFloat(valor)
                    }else{
                        var varString = valor
                    }
                    // alert(VarFloat)
                    // alert(varString)
                    if(AtributeMin<=VarFloat & AtributeMax>=VarFloat){  // Almaceno en listado las dimensiones que se encuentren en el rango
                        // alert(VarFloat)
                        indexDiameter=$(this).text()
                        listado.push(indexDiameter)
                    }

                    if(AtributeString){
                        // alert("Ingreso: "+AtributeString)
                        // alert("Aparece: "+varString)
                        if(varString.toLowerCase().indexOf(AtributeString.toLowerCase()) > -1){
                            // alert("Entra")
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
    // alert(listadoPasar)             // Lo que llega de Atributes y Dimensions
    // alert(listadoAll)            // Cantidad de valores introducidos por filter dimensiones y atributes
    // alert("Entro en Categories")
    compCategories = []
    var catVal = []
    prueba = 5
    // Paginado
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
            // alert($(this).text())
            catVal.push($(this).text())
        }
    })
    for(var i = catVal.length -1; i >=0; i--){
        if(catVal.indexOf(catVal[i]) !== i) catVal.splice(i,1);
    }
    // alert(catVal)       // Filters,SENSOR VVT,Mantenimiento,     Todas las categorias
    // var tamCat = []
    var cont = 0
    inputTotal = 0
    $(this).find("input").each(function(){
        inputTotal = inputTotal + 1
        var aux = $(this).attr("name").split("check")[1]        // Todos los atributos de la base
        // alert(aux)      // Filters - Pumps - Mantenimiento - SENSOR VVT
        if ($("input:checkbox[name="+$(this).attr("name")+"]:checked").val()){
            // alert($(this).attr("name"))                         // checkFilters - checkSENSORVVT
            // alert($(this).attr("name").split("check")[1])       // Filters - SENSORVVT
            // alert($(this).attr("name"))
            comp = $(this).attr("name").split("check")[1]
            compCategories.push(comp)

        }
        else{
            cont = cont +1
        }
    })
    // alert("listadoPasar")            // Atron,Atr2down
    // alert(listadoPasar)             // Atributos y Dimensiones conseguidas, palabras separadas
    // alert("compCategories")          // Filters,SENSORVTV
    // alert(compCategories)           // Categorias seleccionadas, une las palabras
    var contAtrFind = 0
    $("tbody tr").each(function(){      // Recorro por filas
        trnum++//paginado
        var bandShow = false
        // alert("Fila: "+$(this).text())      // Muestro columna
        $(this).find("a").each(function(){      // Recorro por a
            // alert($(this).text())           // Muestro a
            if ($(this).attr("id") == "categoryInfo"){      // Si la columna es Category
                // alert("Entra en Category")
                // alert(compCategories)
                // alert(compCategories.length)
                for(var k=0;k<compCategories.length;k++){ 
                    // alert("this: "+$(this).text().replace(' ','').toLowerCase())    // Lo que tiene la tabla
                    // alert("compCategories j: "+compCategories[k].toLowerCase())
                    // if((compCategories[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
                    if(compCategories[k].toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
                        // alert("Consigue: "+$(this).text())
                        bandShow = true
                        contCategory.push($(this).text())
                    }
                }
            }

            if(listadoPasar.length>0){
                // alert(listadoPasar)
                if($(this).parent().parent().index()==$("#dimensions").index() || $(this).parent().parent().index()==$("#atributes").index()){
                    // aCont++ //paginado
                    // alert("listadoPasar")
                    // alert("Valor actual de tabla: "+$(this).text())
                    // alert(listadoPasar)
                    // alert("Bandera: "+bandShow)
                    for(var i=0; i<listadoPasar.length; i++){
                        if((listadoPasar[i].replace(' ','').toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
                            if(bandShow == true){
                                // listCont++ //paginado
                                // alert($(this).parent().parent().parent().text())
                                // $(this).parent().parent().parent().show()
                                listadoCategory.push($(this).parent().parent().text())
                                // alert("Valor que entra: "+$(this).text())
                                contAtrFind = contAtrFind + 1
                                // alert(contAtrFind)
                                is = true // inventado de paginado
                            }
                            else{
                                is = false //paginado
                            }
                        }
                        // else{
                        //     alert($(this).text())
                        //     contAtrFind = contAtrFind + 1
                        // }
                    }
                }

            }
            if(bandShow == true){
                // alert($(this).text())
                // $(this).show()
                is = true
            }
            
        })
        // listCont = contAtrFind   // Es lo mismo
        // alert("aCont total en tabla")
        // alert(aCont)
        // alert("listCont consigue")
        // alert(listCont)
        // aCont = 0
        // listCont = 0
        
        // alert("Siguiente fila")
        // alert(listadoPasar)             // Dim222 mm,Dim2100 mm   Tener cuidado
        // alert("Cantidad ingresada: "+listadoPasar.length)
        // alert()
        // alert("Cantidad conseguida: "+contAtrFind)           // Valores conseguidos
        // alert(listadoAll) // Cantidad de valores introducidos por filter dimensiones y atributes
        // alert("Bandera: "+bandShow)
        if(listadoPasar.length>0){ // Si trae filtro de dimensiones y atributos
            if ((listadoAll == contAtrFind) && bandShow == true){
                // alert("Show: "+$(this).text())
                // $(this).show() // ESTA SI VA
                // is = true
            }
            else{ // desde aqui es paginacion
                is = false
            }if(is == true){
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
            // else{
            //     is = false
            // }
        }
        else{  // Muestro cuando no trae filtro de dimensiones ni atributos
            if(bandShow == true){
                // $(this).show() // ESTA SI VA
                is = true
            }
            else{
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
            // contAtrFind = 0
        }

        contAtrFind = 0
    }) // fin del tr

    // alert("Sale trnum")
    // alert(trnum)
    // alert("inputTotal: "+inputTotal)
    // alert("Cont: "+cont)
    // alert("catVal: "+catVal)
    // alert("catValLeng: "+catVal.length)
    // alert("inputTotal: "+inputTotal)            // Cantidad total de opciones de Categories
    // alert("cont: "+cont)                        // Cantidad de checks de categories vacíos
    // alert()
    if (inputTotal == cont){      
        // alert("Vacío")      // Si el checkbox está vacío
        if(listadoPasar.length>0){      // Si se ha filtrado antes por dimension o atributos
            contAtrFind = 0
            $("tbody tr").each(function(){
                $($(this).find("a")).each(function(){
                    if($(this).parent().parent().index()==$("#dimensions").index() || $(this).parent().parent().index()==$("#atributes").index()){
                        for(var i=0; i<listadoPasar.length; i++){
                            if((listadoPasar[i].replace(' ','').toLowerCase() == $(this).text().replace(' ','').toLowerCase()) && ($(this).text() != "") && ($(this).text())){
                                // $(this).parent().parent().parent().show()
                                listadoCategory.push($(this).parent().parent().text())
                                contAtrFind = contAtrFind + 1
                            }
                        }
                    }
                })
                if (listadoAll == contAtrFind){
                    // $(this).show() // ESTO SI VA
                    is = true
                }
                else{ // desde aqui es paginacion
                    is = false
                }if(is == true){
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
            $("tbody tr").each(function(){
                trnum++
                // $(this).show() // ESTA SI VA
                // is = true

                // if(bandShow == true){
                //     // $(this).show() // ESTA SI VA
                //     is = true
                // }
                // else{
                //     is = false
                // }
                // alert("trnum")
                // alert(trnum)
                // alert("maxRows")
                // alert(maxRows)
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

                contCategory.push($(this).text())
                // contCategory = []

            })
        }
    }
    // alert(listadoCategory.length)  // Tamaño de filas por filtro de category
    // -------------------------------------------------------------------------------------
    // paginado
    $(".pagination").html("")
    // maxRows = parseInt($("#maxRows").val())
    // alert("listadoCategoryLeng: "+listadoCategory.length)
    // alert("contCategory: "+contCategory.length)
    if(listadoCategory.length>0){
        totalRows = listadoCategory.length
    }
    else{
        totalRows = contCategory.length
    }
    // alert("totalRows")
    // alert(totalRows)
    // alert("contCategory")
    // alert(contCategory.length)
    // alert("maxRows")
    // alert(maxRows)
    // alert("listado")
    // alert(listado)
    // alert(listado.length)
    // alert("listadoCategory")
    // alert(listadoCategory)
    // alert(listadoCategory.length)
    // alert(listadoCategory.length)
    if(totalRows > maxRows){    // TotalRows: 2   maxRows: 1
        // alert("Entra")
        // alert(totalRows)
        // alert(maxRows)
        // Guardo la cantidad de paginas que se necesitan
        // alert("totalRows > maxRows")
        var pagenum = Math.ceil(totalRows/maxRows)
        for(var i=1;i<=pagenum;){
            $(".pagination").append('<li class="page-item" data-page="'+i+'"><a class="page-link" href="#"><span>'+ i++ +'<span class="sr-only">(current)</span></span></a></li>').show()
        }
    }
    $(".pagination li:first-child").addClass("active")

    $(".pagination li").on("click",function(){ // Cuando clickeo la numeración

        // alert("Click")
        // alert(listado)
        var pageNum = $(this).attr("data-page")
        var trIndex = 0;
        var rev = false
        $(".pagination li").removeClass("active")
        $(this).addClass("active")
        // Recorre tolas las filas de la tabla
        $(table+" tr:gt(0)").each(function(){
            // alert("Esto: "+$(this).text())
            trIndex++
            $(this).find("a").each(function(){
                if(listadoPasar.length>0){
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
                }
            })
            if(listadoPasar.length<1){
                rev = true
                if(trIndex > (maxRows*pageNum) || trIndex <= ((maxRows*pageNum)-maxRows)){
                    // alert("Hide: "+$(this).parent().parent().parent().text())
                    $(this).hide()
                }else{
                    $(this).show()
                    // alert("Show: "+$(this).parent().parent().parent().text())
                }
            }
            if(rev===false){
                trIndex--
            }else{
                rev = false
            }

        })
    })
    // -------------------------------------------------------------------------------------

    // listadoAll = inputTotal-cont
    // alert(listadoAll)        // Categories seleccionadas en el checkbox
    // alert(listadoPasar)      // Atron,El Atrdown,materialFOAM,Dim222.0 mm  es listado
    // alert(cont)
    // alert("listCont: "+listCont+" listadoAll: "+listadoAll+" listadoLeng: "+listado.length)
    // alert("Listado: "+listadoCategory)
    for(var x = 0;x < listadoCategory.length; x++){
        pasarCategory.push(listadoCategory[x])
    }
    // alert(listadoCategory.length)
    listadoCategory = []
    contCategory = []
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
    if (listado.length > 0){
        $(".pagination").html("")
        var trnum = 0
        var maxRows = parseInt($("#maxRows").val())
        var semiTotalRows = $(table+" tbody tr").length
        totalRows = listado.length
        var rev = false
        $(table+' tr:gt(0)').each(function(){
            trnum++
            $(this).find("a").each(function(){
                for(var i=0; i<listado.length; i++){

                    if($(this).text()===listado[i]){
                        rev = true
                        if(trnum > maxRows){
                            $(this).parent().parent().parent().hide()
                        }
                        if(trnum <= maxRows){
                            $(this).parent().parent().parent().show()
                        }
                    }
                }
            })
            if(rev===false){
                trnum--
            }else{
                rev = false
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
            var rev = false
            $(".pagination li").removeClass("active")
            $(this).addClass("active")
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
    }else{
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