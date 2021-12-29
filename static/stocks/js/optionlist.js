$(document).ready(function () {
    LoadOptions()
});
function LoadOptions(){
    var url      = window.location.href;
    var params = url.split('/');
    id= params[params.length-1]
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminproducts/" + id,
        type: 'GET',
        dataType: "JSON",

        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('admin')); },
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
            console.log(response['options'])
            const options = response['options'];
            for (let i = 0; i < options.length; i++) {

                table.row.add([options[i].id, options[i].color,
                '<img src="' + options[i].image['extrsmall_square_crop'] + '">', 'Published',
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=loadproducts(' + options[i].id + ')><i class="icofont-edit text-success"></i></a>\
                        <button id='+ options[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=dleteproduct(' + options[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )

            }
            table.draw();
            $('#addoption').show()
            $('#optionorder').val(options.length + 1)
            $('#productID').val(id)
            $('#productName').val(response['name'])
            $('#pageHeadButton').html('<a href="#addproduct" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Product</a>')
            $('#pageHeading').html('<a href="#" onclick="LoadCategories()">Categorie List</a>  >'+'<a href="#" onclick=loadsubcategories('+$("#categoryID").val()+')>'+$("#categoryName").val()+'</a> >  \
            '+'<a href="#" onclick=loadsubsubcategories('+$("#subcategoryID").val()+')>'+$("#subcategoryName").val()+'</a>\
            >  '+'<a href="#" onclick=loadproducts('+$("#subsubcategoryID").val()+')>'+$("#subsubcategoryName").val()+'</a>  >  '+'<a href="#" onclick=loadoptions('+$("#productID").val()+')>'+$("#productName").val()+'</a>')
            return 0;

        },
        error: function (jqXHR) {
        }
    });

}



$('#optionform').submit(function (event) {
    event.preventDefault();
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData(document.getElementById("subsubcategoryform"));
    formData.append("image", $("#optionimage")[0].files[0]);
    formData.append("name", $("#optionname").val());
    formData.append("color", $("#optioncolor").val());
    formData.append("order", $("#optionorder").val());
    formData.append("size", $("#optionsize").val());
    formData.append("stock", $("#optionstock").val());
    formData.append("product", $("#productID").val());
    formData.append("csrfmiddlewaretoken", csrf_token1);
    data = formData
    console.log($("#productorder").val())

    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminoptions/",
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Token ' + localStorage.getItem('token')); },
        success: function (response) {
          LoadOptions()
        },
        error: function (jqXHR) {
            console.log(jqXHR.responseText)
        }

    });
});
