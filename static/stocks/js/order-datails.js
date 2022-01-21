$(document).ready(function () {
    var url = window.location.href;
    var params = url.split('/');
    var id = params[params.length - 1]
    $('#final_msg').hide();
    Orderdetail(id);

});

function Orderdetail(id) {
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminorders/"+id+"/",
        type: 'GET',
        dataType: "JSON",

        success: function (response) {
            console.log(response)

        },
        error: function (jqXHR) {
        }

    });
}

