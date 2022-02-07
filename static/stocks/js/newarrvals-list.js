$(document).ready(function () {
    $('#final_msg').hide()
    LoadNewarrivals()
});
function LoadNewarrivals() {
    $.ajax({
        url: "/stockapi/adminnewarrivals/",
        type: 'GET',
        dataType: "JSON",


        success: function (response) {
            table = $('#myDataTableListProduct').DataTable();
            table
                .rows()
                .remove()
                .draw();
            table.draw();
            table.columns(1).header().to$().text('Product')
            table.columns(2).header().to$().text('Photo')
            table.columns.adjust().draw();
            const products = response;
            for (let i = 0; i < products.length; i++) {
                table.row.add(['<div onclick=loadoptions(' + products[i].product.id + ')>' + products[i].id + '</div>', '<div onclick=loadoptions(' + products[i].product.id + ')>' + products[i].product.name + '</div>',
                '<img src="' + products[i].product.image['extrsmall_square_crop'] + '" onclick=loadoptions(' + products[i].product.id + ')>', '<div onclick=loadoptions(' + products[i].product.id + ')>Published</div>',
                ' <div id='+products[i].id +' class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=editproduct(' + products[i].product.id + ')><i class="icofont-edit text-success"></i></a>\
                        <button id='+ products[i].product.id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=deleterecord(' + products[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )

            }
            table.draw();
            $('#addproduct').show()
            $('#productorder').val(products.length + 1)
            $('#subsubcategoryID').val(id)
            $('#subsubcategoryName').val(response['name'])
            $('#pageHeadButton').html('<a href="#addproduct" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Product</a>')
            $('#pageHeading').html('<a href="#" onclick=LoadNewarrivals(' + $("#subsubcategoryID").val() + ')>' + $("#subsubcategoryName").val() + '</a>')
            return 0;

        },
        error: function (jqXHR) {
        }
    });
    $.ajax({
        url: "/stockapi/productlist/",
        type: 'GET',
        dataType: "JSON",


        success: function (response) {
            for (let i = 0; i < response.length; i++) {
            $('#productToAdd').append('<option value='+response[i].id+'>'+response[i].name+'</option>')
            }
            


        }});
  
}



$('#productform').submit(function (event) {
    event.preventDefault();
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
    var product = $('#productToAdd').val();
    data = {'product':product,csrfmiddlewaretoken:csrf_token1}
    console.log(data)
    $.ajax({
        url: "/stockapi/adminnewarrivals/",
        type: 'POST',
        dataType: "JSON",
        data: data,

        success: function (response) {
            $('#productform').get(0).reset()
            $('#final_msg').fadeIn().delay(1000).fadeOut();
            LoadNewarrivals()
        },
        error: function (jqXHR) {
            console.log(jqXHR.responseText)
        }

    });


});

function deleterecord(id) {
    swal({
        title: "Are you sure?",
        text: "Once deleted, you will not be able to recover datas",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    url: "/stockapi/adminnewarrivals/" + id,
                    type: 'DELETE',
                    dataType: "JSON",


                    success: function (response) {
                        var tablename =$('#myDataTableListProduct').DataTable();
                        tablename
                            .row($('#' + id)
                                .parents('tr'))
                            .remove()
                            .draw();

                    },
                    error: function (jqXHR) {
                    }
                });
            } else {
                swal("Safe");
            }
        });



}







$("#productimage").change(function () {
    $('#submitbutton').show()
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#imageone').attr('src', e.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    }
});


