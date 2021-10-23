
// if ($("#ivaCheck").prop("checked")){
//     // alert("Seleccionado")
//     $("#itbm7").show()
// }
// else{
//     $("#itbm7").hide()
// }

// $("#ivaCheck").on("click",function(){
//     // alert("Cambia")
//     if ($(this).prop("checked")){
//         // alert("Seleccionado")
//         $("#itbm7").show()
//     }
//     else{
//         $("#itbm7").hide()
//     }
// })
// if ($("#ivaCheck").prop("checked")){
//     alert("Seleccionado")
// }

$("#contCatIng").change(function(){
    // alert($(this).find("option:selected").attr("limit").toLowerCase())
    // alert($(this).find("option:selected"))
    // alert($(this).find("option:selected").text())
    // alert($(this).find("option:selected").attr("limit").text())
    // alert($(this).find("option:selected").attr("limit").val())
    // alert($(this).find("option"))
    // alert($(this).find("option").attr("limit"))
    if($(this).find("option:selected").attr("limit").toLowerCase() == "true"){
        $("#divFechaTope").show()
    }
    else{
        $("#divFechaTope").hide()
    }
})

// $("#contCatEgr").change(function(){
//     if($(this).find("option:selected").attr("limit") == "True"){
//         $("#divFechaTope").show()
//     }
//     else{
//         $("#divFechaTope").hide()
//     }
// })

function functionByDay(){
    $("#formByDay").show()
    $("#formByRange").hide()
}

function functionByRange(){
    $("#formByRange").show()
    $("#formByDay").hide()
}

// Para filtrar por name
jQuery(document).ready(function($){
    $(document).ready(function() {
        $('#contNombre').select2();
    });
});

// if ($("#contMonto").val()){
//     total = parseFloat(parseFloat($("#contMonto").val())+parseFloat(parseFloat($("#contMonto").val())*parseFloat(0.07))).toFixed(2)
//     iva = parseFloat(($("#contMonto").val()*0.07)).toFixed(2)
//     $("#contIva").val($("#contMonto").val()+" + "+iva+" = "+total)
// }

$("#contMonto").on("keyup",function(){
    iva=parseFloat(($(this).val()*0.07)).toFixed(2)
    $("#contItbm").val(iva)
    total=parseFloat(parseFloat($(this).val())+parseFloat(iva)).toFixed(2)
    $("#contTotal").val(total)
})
$("#contItbm").on("keyup",function(){
    amount=$("#contMonto").val()
    total=parseFloat(parseFloat(amount)+parseFloat($(this).val())).toFixed(2)
    $("#contTotal").val(total)
    if($(this).val()==""){
        $("#contTotal").val(amount)
    }
})

// $("#contFacType1").click(function(){
//     $("#categoryEntry").show()
//     $("#categorySpending").hide()
// })
// $("#contFacType2").click(function(){
//     $("#categoryEntry").hide()
//     $("#categorySpending").show()
// })

// boton para exportar a Excel -------------------------------------------------------------------------------------
document.getElementById("downloadexcel").addEventListener("click",function(){
    var table2excel = new Table2Excel();
    table2excel.export(document.querySelectorAll("#invoice"));
})

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

// Arreglar por click a cabecera ----------------------------------------------------------------------------------
// Se debe agregar CSS th { cursor: pointer; }
$('th').click(function(){
    var table = $(this).parents('table').eq(0)
    var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()))
    this.asc = !this.asc
    if (!this.asc){rows = rows.reverse()}
    for (var i = 0; i < rows.length; i++){table.append(rows[i])}
})
function comparer(index) {
    return function(a, b) {
        var valA = getCellValue(a, index), valB = getCellValue(b, index)
        return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB)
    }
}
function getCellValue(row, index){ return $(row).children('td').eq(index).text() }

