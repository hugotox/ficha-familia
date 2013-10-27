function bind_datepickers(){
    $('.datepicker').datepicker({
        format: 'dd/mm/yyyy',
        weekStart: 1,
        autoclose: true,
        language: 'es'
    });
}

var round_number = function (number, decimals) {
    if(typeof(decimals) == "undefined"){
        decimals = 2;
    }
    return Math.round(number * Math.pow(10, decimals)) / Math.pow(10, decimals);
};

/**
 * Adds trim() function to string objects (missing in IE)
 */
if(typeof String.prototype.trim !== 'function') {
    String.prototype.trim = function() {
        return this.replace(/^\s+|\s+$/g, '');
    }
}

$(document).ready(function () {
    bind_datepickers();

    $.ajaxSetup({
        cache:false
    });

});