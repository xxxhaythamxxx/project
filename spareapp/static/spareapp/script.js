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

// Funcion para filtrar por medidas -------------------------------------------------------------------
function measureFilter(){

    $("#myTable tr").each(function(){
        $(this).hide();
    })

    var indexDiameter;
    var Diametermin = $("#DiameterMin").val();                                            //Tomo el valor del minimo
    var Diametermax = $("#DiameterMax").val();                                            //Tomo el valor del maximo
    var indexLong;
    var Longmin = $("#LongMin").val();                                            
    var Longmax = $("#LongMax").val();
    var indexHigh;
    var Highmin = $("#HighMin").val();                                            
    var Highmax = $("#HighMax").val();
    var indexWide;
    var Widemin = $("#WideMin").val();                                            
    var Widemax = $("#WideMax").val();
    var listado = []

    $('#myTable tr a').each(function(){
        if($(this).attr("id")==="diameterValue"){
            var text = $(this).text();
            var varSplit = text.split("Diameter: ")
            var DiameterFloat = parseFloat(varSplit[1])
            if(Diametermin<=DiameterFloat & Diametermax>=DiameterFloat){
                indexDiameter=$(this).text()
                listado.push(indexDiameter)
            }
        }
        if($(this).attr("id")==="longValue"){
            var text = $(this).text();
            var varSplit = text.split("Long: ")
            var LongFloat = parseFloat(varSplit[1])
            if(Longmin<=LongFloat & Longmax>=LongFloat){
                indexLong=$(this).text()
                listado.push(indexLong)
            }
        }
        if($(this).attr("id")==="highValue"){
            var text = $(this).text();
            var varSplit = text.split("High: ")
            var HighFloat = parseFloat(varSplit[1])
            if(Highmin<=HighFloat & Highmax>=HighFloat){
                indexHigh=$(this).text()
                listado.push(indexHigh)
            }
        }
        if($(this).attr("id")==="wideValue"){
            var text = $(this).text();
            var varSplit = text.split("Wide: ")
            var WideFloat = parseFloat(varSplit[1])
            if(Widemin<=WideFloat & Widemax>=WideFloat){
                indexWide=$(this).text()
                listado.push(indexWide)
            }
        }
    });
    
    for(var i=0; i<listado.length; i++){
        $("#myTable tr").each(function(){
            $(this).find("a").each(function(){
                if($(this).text()===listado[i]){
                    $(this).parent().parent().parent().show();
                }
            })
        })
    }
    
}

// Funcion resetear valores del filtro de medidas ---------------------------------------------------
function measureReset(){
    // var Diametermin = $("#DiameterMin").val();                                            //Tomo el valor del minimo
    // var Diametermax = $("#DiameterMax").val();                                            //Tomo el valor del maximo
    // var Longmin = $("#LongMin").val();                                            
    // var Longmax = $("#LongMax").val();
    // var Highmin = $("#HighMin").val();                                            
    // var Highmax = $("#HighMax").val();
    // var Widemin = $("#WideMin").val();                                            
    // var Widemax = $("#WideMax").val();

    $("#DiameterMin").val(null);                                            //Tomo el valor del minimo
    $("#DiameterMax").val(null);                                            //Tomo el valor del maximo
    $("#LongMin").val(null);                                            
    $("#LongMax").val(null);
    $("#HighMin").val(null);                                            
    $("#HighMax").val(null);
    $("#WideMin").val(null);                                            
    $("#WideMax").val(null);

    $("#myTable tr").each(function(){
        $(this).show();
    })
}

// Generar PDF desde HTML ----------------------------------------------------------------------------------------
function generatePDF(){
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
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
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
    const element = document.getElementById("invoice");
    
    $("#check").hide();
    $("table td:nth-child("+($("#check").index() + 1)+")").hide();
    $('#invoice tr:first th').each(function() {
        var value = $(this).css("position", "static");
      });
    var opt = {
        margin:       1,
        filename:     'report.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        enableLinks:  true,
        pagebreak:    {mode: "avoid-all"},
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
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
    $("input:checkbox[name=dimensions]").prop("checked",false);
    $("input:checkbox[name=car]").prop("checked",true);
    $("input:checkbox[name=check]").prop("checked",true);
    $("input:checkbox[name=reference]").prop("checked",false);
    $("input:checkbox[name=ecode]").prop("checked",true);
    $("input:checkbox[name=checkDiameter]").prop("checked",false);
    $("input:checkbox[name=checkLong]").prop("checked",false);
    $("input:checkbox[name=checkHigh]").prop("checked",false);
    $("input:checkbox[name=checkWide]").prop("checked",false);

    $("#photo").show();
    $("table td:nth-child("+($("#photo").index() + 1)+")").show();
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
    $("#dimensions").hide();
    $("table td:nth-child("+($("#dimensions").index() + 1)+")").hide();
    $("#reference").hide();
    $("table td:nth-child("+($("#reference").index() + 1)+")").hide();
    $("#ecode").show();
    $("table td:nth-child("+($("#ecode").index() + 1)+")").show();
    $("#DiameterFilter").hide();
    $("#LongFilter").hide();
    $("#HighFilter").hide();
    $("#WideFilter").hide();
    $("#ButtonFilter").hide();

    $("#myTable tr").each(function(){
        $(this).show();
    })
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
$("input:checkbox[name=dimensions]").prop("checked",false);
$("input:checkbox[name=reference]").prop("checked",false);
$("input:checkbox[name=car]").prop("checked",true);
$("input:checkbox[name=check]").prop("checked",true);
$("input:checkbox[name=ecode]").prop("checked",true);

$List.change(function(){
    
    let detailidi = $("#detail-id").index();
    let photoi = $("#photo").index();
    let codei = $("#code").index();
    let brandi = $("#brand").index();
    let typei = $("#type").index();
    let cari = $("#car").index();
    let shapei = $("#shape").index();
    let dimensionsi = $("#dimensions").index();
    let referencei = $("#reference").index();
    let checki = $("#check").index();
    let ecodei = $("#ecode").index();
    
    if ($("input:checkbox[name=detail-id]:checked").val()){
        $("#detail-id").show();
        $("table td:nth-child("+(detailidi + 1)+")").show();
    }else{
        $("#detail-id").hide();
        $("table td:nth-child("+(detailidi + 1)+")").hide();
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
});

// Menu de filtrar por medidas ---------------------------------------------------------------------------
const $List2 = $("#headerList2");
$("input:checkbox[name=checkDiameter]").prop("checked",false);
$("input:checkbox[name=checkLong]").prop("checked",false);
$("input:checkbox[name=checkHigh]").prop("checked",false);
$("input:checkbox[name=checkWide]").prop("checked",false);

$List2.change(function(){
    
    if ($("input:checkbox[name=checkDiameter]:checked").val()){
        $("#DiameterFilter").show();
    }else{
        $("#DiameterFilter").hide();
    }
    if ($("input:checkbox[name=checkLong]:checked").val()){
        $("#LongFilter").show();
    }else{
        $("#LongFilter").hide();
    }
    if ($("input:checkbox[name=checkHigh]:checked").val()){
        $("#HighFilter").show();
    }else{
        $("#HighFilter").hide();
    }
    if ($("input:checkbox[name=checkWide]:checked").val()){
        $("#WideFilter").show();
    }else{
        $("#WideFilter").hide();
    }
    if ($("input:checkbox[name=checkDiameter]:checked").val() || $("input:checkbox[name=checkLong]:checked").val() || $("input:checkbox[name=checkHigh]:checked").val() || $("input:checkbox[name=checkWide]:checked").val()){
        $("#ButtonFilter").show();
    }else{
        $("#ButtonFilter").hide();
    }
})

// Tabla sorteable ----------------------------------------------------------------------------------
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
                $(this).text(i);
                i=i+1;
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
