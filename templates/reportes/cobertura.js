
function create_cobertura_chart(tipo){
    $.getJSON("/reportes/"+anio+"/cobertura/"+tipo+"/", function(data){
        data.chart.renderTo = "div-grafico-cobertura";
        var chart = new Highcharts.Chart(data);
    });
}

create_cobertura_chart("familias");

$("#select_cobertura_tipo").change(function(){
    create_cobertura_chart($(this).val());
});


