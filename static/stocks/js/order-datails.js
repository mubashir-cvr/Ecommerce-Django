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
            $('#address').html(response.address)
            $('#pincode').html(response.pincode)
            $('#phone').html(response.phone)
            $('#phone').html(response.phone)
            $('#nameofproduct').html(response.product.name)
            $('#quantity').html(response.quantity)
            $('#orderstatus').val(response.status)
            if(response.has_paid){
                $('#paymentStatus').val("Completed")
            }
            else{
                $('#paymentStatus').val("Fail")
            }

            $('#unitprice').html(response.amount +" "+response.currency)
            if(response.selectedcolor){
                $("#productImg").attr("src", response.selectedcolor.image_one.extrsmall_square_crop);
            }
            else{
                $("#productImg").attr("src", response.product.image.extrsmall_square_crop);
            }


        },
        error: function (jqXHR) {
        }

    });
}

