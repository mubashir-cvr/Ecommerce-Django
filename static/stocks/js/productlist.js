$(document).ready(function () {
    Loadproducts()
});
function Loadproducts(){
    var url      = window.location.href;
    var params = url.split('/');
    id= params[params.length-1]
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminsubsubcategories/" + id,
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
            const products = response['products'];
            for (let i = 0; i < products.length; i++) {
    
                table.row.add(['<div onclick=loadoptions(' +products[i].id+')>'+products[i].id+'</div>','<div onclick=loadoptions(' +products[i].id+')>'+products[i].name+'</div>',
                '<img src="' + products[i].image['extrsmall_square_crop'] + '" onclick=loadoptions(' +products[i].id+')>', '<div onclick=loadoptions(' +products[i].id+')>Published</div>',
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=editproduct(' + products[i].id + ')><i class="icofont-edit text-success"></i></a>\
                        <button id='+ products[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=deleteproduct(' + products[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )
    
            }
            table.draw();
            $('#addproduct').show()
            $('#productorder').val(products.length + 1)
            $('#subsubcategoryID').val(id)
            $('#subsubcategoryName').val(response['name'])
            $('#pageHeadButton').html('<a href="#addproduct" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Product</a>')
            $('#pageHeading').html('<a href="#" onclick=loadproducts('+$("#subsubcategoryID").val()+')>'+$("#subsubcategoryName").val()+'</a>')
            return 0;
    
        },
        error: function (jqXHR) {
        }
    });
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/brandlist/",
        type: 'GET',
        dataType: "JSON",
    
        
        success: function (response) {
            
            for (let i = 0; i < response.length; i++) {
    
                $('#priductbrand').append("<option value="+response[i].id+">"+response[i].name+"</option>")
    
            }
        },
        error: function (jqXHR) {
        }
    });
}



$('#productform').submit(function (event) {
    event.preventDefault();
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData(document.getElementById("productform"));
    formData.append("image", $("#productimage")[0].files[0]);
    formData.append("name", $("#productname").val());
    formData.append("price", $("#productprice").val());
    if( $('#priductbrand').val()!=0){
        formData.append("brand", $("#priductbrand").val());
    }
    formData.append("order", $("#productorder").val());
    formData.append("subsubcategory", $("#subsubcategoryID").val());
    formData.append("csrfmiddlewaretoken", csrf_token1);
    data = formData

    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminproducts/",
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        
        success: function (response) {
            if($('#productofferprice').val()!=''){
            var offprice=$('#productofferprice').val()
            var data={
                "offerPrice":offprice,
                "product":response.id,
            }
            $.ajax({
                url: "http://127.0.0.1:8000/stockapi/addoffers/",
                type: 'POST',
                data: data,
                dataType:'JSON',
                
                success: function (response) {
                    $('#productform').get(0).reset()
$("img").attr("src","https://dummyimage.com/150x200.gif")
                    Loadproducts()
                },
                error: function (jqXHR) {
                    console.log(jqXHR.responseText)
                }
        
            });
        }
        else{
            $('#productform').get(0).reset()
$("img").attr("src","https://dummyimage.com/150x200.gif")
        Loadproducts()
        }
        $('#productform').get(0).reset()
$("img").attr("src","https://dummyimage.com/150x200.gif")
        Loadproducts()
        },
        error: function (jqXHR) {
            console.log(jqXHR.responseText)
        }

    });

    
});

function deleteproduct(id) {
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
        url: "http://127.0.0.1:8000/stockapi/deleteproduct/" + id,
        type: 'DELETE',
        dataType: "JSON",

        
        success: function (response) {
            var tablename = $('#' + id).closest('table').DataTable();
            tablename
                .row($('#' + id)
                    .parents('tr'))
                .remove()
                .draw();

        },
        error: function (jqXHR) {
        }
    });
}else {
    swal("Safe");
}
});



}






function loadoptions(id) {
    window.location="http://127.0.0.1:8000/stocks/listoptions/"+id
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


function editproduct(id) {
    window.location="http://127.0.0.1:8000/stocks/editproducts/"+id
}