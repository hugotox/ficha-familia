function bind_datepickers(){
    $('.datepicker').datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd/mm/yy",
        firstDay: 1
    });
}

var round_number = function (number, decimals) {
    return Math.round(number * Math.pow(10, decimals)) / Math.pow(10, decimals);
};

$(document).ready(function () {
    bind_datepickers();
});