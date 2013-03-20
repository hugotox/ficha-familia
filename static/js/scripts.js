function bind_datepickers(){
    $('.datepicker').datepicker({
        format: 'dd/mm/yyyy',
        weekStart: 1,
        autoclose: true,
        language: 'es'
    });
}

var round_number = function (number, decimals) {
    return Math.round(number * Math.pow(10, decimals)) / Math.pow(10, decimals);
};

$(document).ready(function () {
    bind_datepickers();
});