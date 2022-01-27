$(document).ready(function () {
    var url = window.location.href;
    var params = url.split('/');
    var id = params[params.length - 1]
    $('#final_msg').hide();
    Orderdetail(id);

});

function Orderdetail(id) {
    $.ajax({
        url: "/stockapi/adminorders/"+id+"/",
        type: 'GET',
        dataType: "JSON",

        success: function (response) {
            console.log(response)
            $('#address').html(response.address)
            $('#pincode').html(response.pincode)
            $('#nameOfCustomer').html(response.firstName)
            $('#emailOfCustomer').html(response.email)
            $('#createdat').html(response.created_on)
            $('#customerContact').html(response.phone)
            $('#phone').html(response.phone)
            $('#phone').html(response.phone)
            $('#nameofproduct').html(response.product.name)
            $('#quantity').html(response.quantity)
            $('#orderstatus').val(response.status)
            $('#expectedDateView').html(response.expected_delivery)
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

$('#orderUpdate').submit(function (event) {
    var url = window.location.href;
    var params = url.split('/');
    var id = params[params.length - 1]
    event.preventDefault();
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
        var formData = new FormData(document.getElementById("orderUpdate"));
        formData.append("expected_delivery", $("#dateofdelivery").val());
        formData.append("status", $("#orderstatus").val());
        
        formData.append("csrfmiddlewaretoken", csrf_token1);
    $.ajax({
        url: "/stockapi/adminorders/"+id+"/",
        type: 'PATCH',
        data: formData,
        processData: false,
        contentType: false,
        
        success: function (response) {

            $('#final_msg').fadeIn().delay(1000).fadeOut();
            Orderdetail(id);
        },
        error: function (jqXHR) {
            console.log(JSON.stringify(jqXHR))
        }

    });
});