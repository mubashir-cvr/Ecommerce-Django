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
            console.log(response)
            table = $('#myDataTable').DataTable();
            table
                .rows()
                .remove()
                .draw();
            table.columns(1).header().to$().text('Product')
            table.columns(2).header().to$().text('Photo')
            table.columns.adjust().draw();
            console.log(response['products'])
            const products = response['products'];
            for (let i = 0; i < products.length; i++) {
    
                table.row.add([products[i].id, products[i].name,
                '<img src="' + products[i].image['extrsmall_square_crop'] + '">', 'Published',
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=loadoptions(' + products[i].id + ')><i class="icofont-edit text-success"></i></a>\
                        <button id='+ products[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=dleteproduct(' + products[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )
    
            }
            table.draw();
            $('#addproduct').show()
            $('#productorder').val(products.length + 1)
            $('#subsubcategoryID').val(id)
            $('#subsubcategoryName').val(response['name'])
            $('#pageHeadButton').html('<a href="#addproduct" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Product</a>')
            $('#pageHeading').html('<a href="#" onclick="LoadCategories()">Categorie List</a>  >'+'<a href="#" onclick=loadsubcategories('+$("#categoryID").val()+')>'+$("#categoryName").val()+'</a> >  \
            '+'<a href="#" onclick=loadsubsubcategories('+$("#subcategoryID").val()+')>'+$("#subcategoryName").val()+'</a>\
            >  '+'<a href="#" onclick=loadproducts('+$("#subsubcategoryID").val()+')>'+$("#subsubcategoryName").val()+'</a>')
            return 0;
    
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
    formData.append("order", $("#productorder").val());
    formData.append("subsubcategory", $("#subsubcategoryID").val());
    formData.append("csrfmiddlewaretoken", csrf_token1);
    data = formData
    console.log($("#productorder").val())

    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminproducts/",
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        
        success: function (response) {
            Loadproducts()
        },
        error: function (jqXHR) {
            console.log(jqXHR.responseText)
        }

    });
});

function dleteproduct(id) {

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



}





function loadoptions(id) {
    window.location="http://127.0.0.1:8000/stocks/listoptions/"+id
}