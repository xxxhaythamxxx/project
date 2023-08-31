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

// Funcion resetear valores del filtro de medidas ---------------------------------------------------
function measureReset(){

    $("#headerList2").each(function(){      // Dimensiones
        $(this).find("input").each(function(){
            var aux = $(this).attr("name").split("check")[1]
            $("#"+aux+"Min").val(null);
            $("#"+aux+"Max").val(null);
        })
    })
    $("#headerList3").each(function(){      // Atributos
        $(this).find("input").each(function(){
            var aux = $(this).attr("name").split("check")[1]
            $("#"+aux).val(null);
        })
    })

    $("#headerList5").each(function(){              // Categories
        $(this).find("input").each(function(){
            $(this).prop("checked",false);
        })
    })

    $("#headerList6").each(function(){              // Vendors
        $(this).find("input").each(function(){
            $(this).prop("checked",false);
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


// $("#secondFormSubmit").on("click",function(a){
//     alert("ENtra")
//     a.preventDefault()
// })

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

//  Filtrar spare references -----------------------------------------------------------------
$("#referenc").on("keyup",function(){                                // Cuando se teclea algo
    // alert("Toma")
    var value = $(this).val().toLowerCase();                        // Toma el valor del input en minuscula
    $("#codPasar option").filter(function(){                             // 
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    })
})

//  Filtrar car info ----------------------------------------------------------------------
$("#carinf").on("keyup",function(){       
    var value = $(this).val().toLowerCase();
    $("#carcodPasar option").filter(function(){
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    })
})

// Filtrar car en FillEngine
$("#engcarinf").on("keyup",function(){       
    var value = $(this).val().toLowerCase();
    $("#engcarcodPasar option").filter(function(){
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    })
})

//  Filtrar engine info ----------------------------------------------------------------------
$("#enginf").on("keyup",function(){       
    var value = $(this).val().toLowerCase();
    $("#enginecodPasar option").filter(function(){
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    })
})

//  Filtrar vendors ----------------------------------------------------------------------
$("#vendorinf").on("keyup",function(){       
    var value = $(this).val().toLowerCase();
    $("#vendorcodPasar option").filter(function(){
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    })
})
// Mostrar a ambos lados los references que se tienen -------------------------------------
$("#codPasar option").each(function(){
    var aux = $(this).text()
    var band = false
    $("#codPasado option").each(function(){
        if($(this).text() == aux){
            band = true
        }
    })
    if (band == true){
        $(this).remove()
        // $(this).hide()
    }
})

// Mostrar a ambos lados los vendors que se tienen -------------------------------------
$("#vendorPasar option").each(function(){
    var aux = $(this).text()
    var band = false
    $("#vendorPasado option").each(function(){
        if($(this).text() == aux){
            band = true
        }
    })
    if (band == true){
        $(this).remove()
        // $(this).hide()
    }
})

// Mostrar a ambos lados los car info que se tienen -------------------------------------
$("#carcodPasar option").each(function(){
    var aux = $(this).text()
    var band = false
    $("#carcodPasado option").each(function(){
        if($(this).text() == aux){
            band = true
        }
    })
    if (band == true){
        $(this).remove()
        // $(this).hide()
    }
})

// Mostrar a ambos lados los car info que se tienen en fillEngine -------------------------------------
$("#engcarcodPasar option").each(function(){
    var aux = $(this).text()
    var band = false
    $("#engcarcodPasado option").each(function(){
        if($(this).text() == aux){
            band = true
        }
    })
    if (band == true){
        $(this).remove()
        // $(this).hide()
    }
})

// Mostrar a ambos lados los engine info que se tienen -------------------------------------
$("#enginecodPasar option").each(function(){
    var aux = $(this).text()
    var band = false
    $("#enginecodPasado option").each(function(){
        if($(this).text() == aux){
            band = true
        }
    })
    if (band == true){
        $(this).remove()
        // $(this).hide()
    }
})
// Pasar de un lado a otro los spares references ---------------------------------------------
function pasar(){
    $("#codPasar option:selected").each(function(){ // Recorre lista sin pasar
        band = false
        var aux = $(this).text()
        $("#codPasado option").each(function(){ // Recorre lista pasada
            if(aux == $(this).text()){
            }
            else{
                band = true
                aux2 = aux
            }
            
        })
        if($("#codPasado option:selected").length<1){
            band = true
            aux2 = aux
        }
        $(this).remove()
        if(band == true){
            $("#codPasado").prepend("<option class='p-1'>"+aux2+"</option>")
        }
    })
}
function regresar(){
    $("#codPasado option:selected").each(function(){ // Recorre lista pasada
        band = false
        var aux = $(this).text()
        $("#codPasar option").each(function(){ // Recorre lista sin pasar
            if(aux == $(this).text()){
            }
            else{
                band = true
                aux2 = aux
            }
        })
        if($("#codPasar option:selected").length<1){
            band = true
            aux2 = aux
        }
        $(this).remove()
        if(band == true){
            $("#codPasar").prepend("<option class='p-1'>"+aux2+"</option>")
        }
    })
    
}

// Pasar de un lado a otro los car info  --------------------------------------------------
function carpasar(){
    $("#carcodPasar option:selected").each(function(){ // Recorre lista sin pasar
        band = false
        var aux = $(this).text()
        $("#carcodPasado option").each(function(){ // Recorre lista pasada
            if(aux == $(this).text()){
            }
            else{
                band = true
                aux2 = aux
            }
            
        })
        if($("#carcodPasado option:selected").length<1){
            band = true
            aux2 = aux
        }
        $(this).remove()
        if(band == true){
            $("#carcodPasado").prepend("<option class='p-1'>"+aux2+"</option>")
        }
    })
}
function carregresar(){
    $("#carcodPasado option:selected").each(function(){ // Recorre lista pasada
        band = false
        var aux = $(this).text()
        $("#carcodPasar option").each(function(){ // Recorre lista sin pasar
            if(aux == $(this).text()){
            }
            else{
                band = true
                aux2 = aux
            }
        })
        if($("#carcodPasar option:selected").length<1){
            band = true
            aux2 = aux
        }
        $(this).remove()
        if(band == true){
            $("#carcodPasar").prepend("<option class='p-1'>"+aux2+"</option>")
        }
    })
}

// Pasar de un lado a otro los car info en FillSpare --------------------------------------
function engcarpasar(){
    $("#engcarcodPasar option:selected").each(function(){ // Recorre lista sin pasar
        band = false
        var aux = $(this).text()
        $("#engcarcodPasado option").each(function(){ // Recorre lista pasada
            if(aux == $(this).text()){
            }
            else{
                band = true
                aux2 = aux
            }
            
        })
        if($("#engcarcodPasado option:selected").length<1){
            band = true
            aux2 = aux
        }
        $(this).remove()
        if(band == true){
            $("#engcarcodPasado").prepend("<option class='p-1'>"+aux2+"</option>")
        }
    })
}
function engcarregresar(){
    $("#engcarcodPasado option:selected").each(function(){ // Recorre lista pasada
        band = false
        var aux = $(this).text()
        $("#engcarcodPasar option").each(function(){ // Recorre lista sin pasar
            if(aux == $(this).text()){
            }
            else{
                band = true
                aux2 = aux
            }
        })
        if($("#engcarcodPasar option:selected").length<1){
            band = true
            aux2 = aux
        }
        $(this).remove()
        if(band == true){
            $("#engcarcodPasar").prepend("<option class='p-1'>"+aux2+"</option>")
        }
    })
}

// Pasar de un lado a otro los vendors  ---------------------------------------------
function vendorpasar(){
    $("#vendorPasar option:selected").each(function(){ // Recorre lista sin pasar
        band = false
        var aux = $(this).text()
        $("#vendorPasado option").each(function(){ // Recorre lista pasada
            if(aux == $(this).text()){
            }
            else{
                band = true
                aux2 = aux
            }
            
        })
        if($("#vendorPasado option:selected").length<1){
            band = true
            aux2 = aux
        }
        $(this).remove()
        if(band == true){
            $("#vendorPasado").prepend("<option class='p-1'>"+aux2+"</option>")
        }
    })
}
function vendorregresar(){
    $("#vendorPasado option:selected").each(function(){ // Recorre lista pasada
        band = false
        var aux = $(this).text()
        $("#vendorPasar option").each(function(){ // Recorre lista sin pasar
            if(aux == $(this).text()){
            }
            else{
                band = true
                aux2 = aux
            }
        })
        if($("#vendorPasar option:selected").length<1){
            band = true
            aux2 = aux
        }
        $(this).remove()
        if(band == true){
            $("#vendorPasar").prepend("<option class='p-1'>"+aux2+"</option>")
        }
    })
    
}

// Pasar de un lado a otro los engine info  --------------------------------------------------
function enginepasar(){
    $("#enginecodPasar option:selected").each(function(){ // Recorre lista sin pasar
        band = false
        var aux = $(this).text()
        $("#enginecodPasado option").each(function(){ // Recorre lista pasada
            if(aux == $(this).text()){
            }
            else{
                band = true
                aux2 = aux
            }
            
        })
        if($("#enginecodPasado option:selected").length<1){
            band = true
            aux2 = aux
        }
        $(this).remove()
        if(band == true){
            $("#enginecodPasado").prepend("<option class='p-1'>"+aux2+"</option>")
        }
    })
}
function engineregresar(){
    $("#enginecodPasado option:selected").each(function(){ // Recorre lista pasada
        band = false
        var aux = $(this).text()
        $("#enginecodPasar option").each(function(){ // Recorre lista sin pasar
            if(aux == $(this).text()){
            }
            else{
                band = true
                aux2 = aux
            }
        })
        if($("#enginecodPasar option:selected").length<1){
            band = true
            aux2 = aux
        }
        $(this).remove()
        if(band == true){
            $("#enginecodPasar").prepend("<option class='p-1'>"+aux2+"</option>")
        }
    })
}

// reftam = 1
// Agregar ref codes
$("#addRef").click(function(){
    $("#reference-content")
    .append('<div id="ref-val" class="ref-val row">\
        <div class="col-lg-11">\
            <div class="row">\
                <div class="col-lg-6">\
                    <input placeholder="Add the reference code" value="" type="text" class="form-control" name="refcodes" id="refcodes" aria-describedby="refcodesHelp" maxlength="80">\
                </div>\
                <div class="col-lg-5">\
                    <input placeholder="Add a note" value="" type="text" class="form-control" name="refcodesnote" id="refcodesnote" aria-describedby="refcodesnoteHelp" maxlength="80">\
                </div>\
                <div class="col-lg-1 d-flex justify-content-center align-items-center">\
                    <input type="checkbox">\
                </div>\
            </div>\
        </div>\
        <div class="col-lg-1 d-flex justify-content-center align-items-center">\
            <div>\
                <a style="text-decoration: none;color: rgb(136,12,12);" id="deleteRef" class="p-2" href="javascript:void(0);">\
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-dash-circle-fill" viewBox="0 0 16 16">\
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM4.5 7.5a.5.5 0 0 0 0 1h7a.5.5 0 0 0 0-1h-7z"/>\
                    </svg>\
                </a>\
            </div>\
        </div>\
    </div>\
        '
        )
})
// Eliminar ref codes
$("#reference-content").on("click","#deleteRef",function(a){
    a.preventDefault()
    $(this).parent().parent().parent().remove()
    // reftam--
})

// Eliminar Atributes
$("#atribute-content").on("click","#atributdeleteRef",function(a){
    a.preventDefault()
    $(this).parent().parent().parent().remove()
    // atrtam--
})

// Agregar dimensiones
$("#dimensaddRef").click(function(){
    $("#dimension-content")
    .append(
        // '<div id="ref-val" class="ref-val row"><div class="col-lg-11"><input placeholder="Add the dimension name" value="" type="text" class="form-control" name="dimensName" id="dimensName" aria-describedby="dimensNameHelp" maxlength="80"><input placeholder="Add the dimension value" value="" type="number" class="form-control" name="dimensVal" id="dimensVal" aria-describedby="dimensValHelp" maxlength="80"></div><div class="col-lg-1 d-flex justify-content-center align-items-center"><div><a style="text-decoration: none;color: rgb(136,12,12);" id="dimesdeleteRef" class="p-2" href="javascript:void(0);"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-dash-circle-fill" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM4.5 7.5a.5.5 0 0 0 0 1h7a.5.5 0 0 0 0-1h-7z"/></svg></a></div></div></div>'
        '<div id="ref-val" class="ref-val row"><div class="col-lg-11"><div class="row"><div class="col-lg-6"><input placeholder="Add the dimension name" value="" type="text" class="form-control" name="dimensName" id="dimensName" aria-describedby="dimensNameHelp" maxlength="80"></div><div class="col-lg-6"><input placeholder="Add the dimension value" value="" type="number" class="form-control" name="dimensVal" id="dimensVal" aria-describedby="dimensValHelp" maxlength="80"></div></div></div><div class="col-lg-1 d-flex justify-content-center align-items-center"><div><a style="text-decoration: none;color: rgb(136,12,12);" id="dimesdeleteRef" class="p-2" href="javascript:void(0);"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-dash-circle-fill" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM4.5 7.5a.5.5 0 0 0 0 1h7a.5.5 0 0 0 0-1h-7z"/></svg></a></div></div></div>'
        )
})
// Eliminar dimensiones
$("#dimension-content").on("click","#dimesdeleteRef",function(a){
    a.preventDefault()
    $(this).parent().parent().parent().remove()
})

// Confirmar eliminar

// $("#deleteSpare").on("click",function(){
//     var mensaje;
//     var opcion = confirm("¿Deseas eliminar el repuesto?");
//     if (opcion == true) {
//         mensaje = "Has clickado OK";
// 	} else {
// 	    mensaje = "Has clickado Cancelar";
//     }
//     // alert(mensaje)
//     // confirm("Has eliminado el repuesto")
// })


// Boton default para que reinicie la tabla ------------------------------------------------------------------------
document.getElementById("default").addEventListener("click",function(){
    
    $("input:checkbox[name=photo]").prop("checked",true);
    $("input:checkbox[name=code]").prop("checked",false);
    $("input:checkbox[name=car]").prop("checked",true);
    $("input:checkbox[name=brand]").prop("checked",false);
    $("input:checkbox[name=type]").prop("checked",false);
    $("input:checkbox[name=shape]").prop("checked",false);
    $("input:checkbox[name=dimensions]").prop("checked",false);
    $("input:checkbox[name=atributes]").prop("checked",true);
    $("input:checkbox[name=category]").prop("checked",true);
    $("input:checkbox[name=priceM]").prop("checked",false);
    $("input:checkbox[name=priceD]").prop("checked",false);
    $("input:checkbox[name=check]").prop("checked",true);
    $("input:checkbox[name=referenceC]").prop("checked",true);
    $("input:checkbox[name=editSpare]").prop("checked",true);
    $("input:checkbox[name=engine]").prop("checked",true);
    $("input:checkbox[name=ecode]").prop("checked",true);

    $("#headerList2").each(function(){              // Dimensions
        $(this).find("input").each(function(){
            var comp = $(this).attr("name")
            $(this).prop("checked",false);
        })
    })
    $("#headerList3").each(function(){              // Atributes
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
    $("#code").hide();
    $("table td:nth-child("+($("#code").index() + 1)+")").hide();
    $("#car").show();
    $("table td:nth-child("+($("#car").index() + 1)+")").show();
    $("#brand").hide();
    $("table td:nth-child("+($("#brand").index() + 1)+")").hide();
    $("#type").hide();
    $("table td:nth-child("+($("#type").index() + 1)+")").hide();
    $("#car").show();
    $("table td:nth-child("+($("#car").index() + 1)+")").show();
    $("#check").show();
    $("table td:nth-child("+($("#check").index() + 1)+")").show();
    $("#shape").hide();
    $("table td:nth-child("+($("#shape").index() + 1)+")").hide();
    $("#dimensions").hide();
    $("table td:nth-child("+($("#dimensions").index() + 1)+")").hide();
    $("#atributes").show();
    $("table td:nth-child("+($("#atributes").index() + 1)+")").show();
    $("#referenceC").show();
    $("table td:nth-child("+($("#referenceC").index() + 1)+")").show();
    $("#editSpare").show();
    $("table td:nth-child("+($("#editSpare").index() + 1)+")").show();
    $("#engine").show();
    $("table td:nth-child("+($("#engine").index() + 1)+")").show();
    $("#category").show();
    $("table td:nth-child("+($("#category").index() + 1)+")").show();
    $("#ecode").show();
    $("table td:nth-child("+($("#ecode").index() + 1)+")").show();

    $("#headerList2").each(function(){                  // Dimensions
        $(this).find("input").each(function(){

            var aux = $(this).attr("name").split("check")[1]
            $("#"+aux+"Filter").hide();
        })
    })
    $("#headerList3").each(function(){                  // Atributes
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
    // if(table2excel){
    //     $("#check").show();
    // }
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
$("input:checkbox[name=code]").prop("checked",false);
$("input:checkbox[name=car]").prop("checked",true);
$("input:checkbox[name=brand]").prop("checked",false);
$("input:checkbox[name=type]").prop("checked",false);
$("input:checkbox[name=shape]").prop("checked",false);
$("input:checkbox[name=dimensions]").prop("checked",false);
$("input:checkbox[name=atributes]").prop("checked",true);
$("input:checkbox[name=referenceC]").prop("checked",true);
$("input:checkbox[name=editSpare]").prop("checked",true);
$("input:checkbox[name=engine]").prop("checked",true);
$("input:checkbox[name=priceM]").prop("checked",false);
$("input:checkbox[name=priceD]").prop("checked",false);
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
    let referencei = $("#referenceC").index();
    let editSparei = $("#editSpare").index();
    let enginei = $("#engine").index();
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

    if ($("input:checkbox[name=referenceC]:checked").val()){
        $("#referenceC").show();
        $("table td:nth-child("+(referencei + 1)+")").show();
    }else{
        $("#referenceC").hide();
        $("table td:nth-child("+(referencei + 1)+")").hide();
    }

    if ($("input:checkbox[name=editSpare]:checked").val()){
        $("#editSpare").show();
        $("table td:nth-child("+(editSparei + 1)+")").show();
    }else{
        $("#editSpare").hide();
        $("table td:nth-child("+(editSparei + 1)+")").hide();
    }

    if ($("input:checkbox[name=engine]:checked").val()){
        $("#engine").show();
        $("table td:nth-child("+(enginei + 1)+")").show();
    }else{
        $("#engine").hide();
        $("table td:nth-child("+(enginei + 1)+")").hide();
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
        $(this).prop("checked",false);
    })
})

const $List5 = $("#headerList5");       // Categories
$("#headerList5").each(function(){
    $(this).find("input").each(function(){
        // var comp = $(this).attr("name")
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

$List3.change(function(){           // Activar filtro de atributos

    $(".filterAtr").each(function(){
        $(this).hide()
    })

    auxAtr = []

    $(this).find("input:checked").each(function(){
        auxAtr = []
        var aux = $(this).parent().find("label").text()
        $("#myTable td").find("#AtrName").each(function(){
            if($(this).text()==aux+":"){
                auxAtr.push($(this).parent().find("#AtrVal").text())
            }
        })
        auxAtr = new Set(auxAtr)
        auxAtr = [...auxAtr].sort();
        $(".filterAtr input[placeholder='"+$(this).parent().find("label").text()+"']").parent().parent().show()
        $(".filterAtr input[placeholder='"+$(this).parent().find("label").text()+"']").parent().find("button").attr("data-bs-content",auxAtr)
        $("#ButtonFilter").show();
    })

    if($(this).find("input:checked").length<1){
        $("#ButtonFilter").hide();
    }
    
})

$List5.change(function(){           // Activar filtro de Categories

    measureFilter()

})


$List6.change(function(){           // Activar filtro de Vendors
    for(var i = listadoPasar.length -1; i >=0; i--){
        if(listadoPasar.indexOf(listadoPasar[i]) !== i) listadoPasar.splice(i,1);
    }
    compVendors = []
    contVendor = []
    contCategory = []
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
                        if(compCategories[k].replace(' ','').toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
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
            }   // No trae nada de Dimension o atributos
            if ($(this).attr("id") == "vendorInfo"){      // Si la columna es Vendor
                for(var k=0;k<compVendors.length;k++){ 
                    if(compVendors[k].replace(' ','').toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
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
    if (inputTotal == cont){        // Si el checkbox Vendors está vacío    
        if(listadoPasar.length>0){      // Si se ha filtrado antes por dimension o atributos
            trnum = 0
            is = false
            $("tbody tr").each(function(){
                bandShow2 = false
                trnum++
                contAtrFind = 0
                $(this).find("a").each(function(){

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
                                if(compCategories[k].replace(' ','').toLowerCase() == $(this).text().replace(' ','').toLowerCase()){
                                    bandShow2 = true
                                    // contCategory.push($(this).text())
                                }
                            }
                        }
                    }
                }) // Fin a
                if ((listadoAll == contAtrFind)){   // Si consigue todos los atr y dim
                    if(compCategories.length>0){    // Si hay check de category
                        if(bandShow2 == true){      // Si consiguió category
                            is = true
                            contTotalTable.push($(this).text())
                            listadoCategory.push($(this).text())
                        }
                    }
                    else{   // Si no hay check de category
                        is = true
                        contTotalTable.push($(this).text())
                        listadoCategory.push($(this).text())
                    }
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
                is = false // hasta aqui
            })
        }
        else{           // Si no se ha filtrado por atributos o dimensiones
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
    for(var x = 0;x < listadoCategory.length; x++){
        pasarCategory.push(listadoCategory[x])
    }
    listadoCategory = []

})

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
            })
        }
    })
        
})


