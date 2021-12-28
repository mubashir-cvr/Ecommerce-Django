$(document).ready(function () {

    LoadCategories()
});

function hideforms() {
    $('#addcategory').hide()
    $('#addsubcategory').hide()
    $('#addsubsubcategory').hide()
    $('#addproduct').hide()

}
function LoadCategories() {
    hideforms();
    $('#addcategory').show()
    table = $('#myDataTable').DataTable();
    table
        .rows()
        .remove()
        .draw();
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/admincategories/",
        type: 'GET',
        dataType: "JSON",

        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('admin')); },
        success: function (response) {
            const categories = JSON.parse(JSON.stringify(response));
            for (let i = 0; i < categories.length; i++) {

                table.row.add([categories[i].id, categories[i].name,
                    'March 13, 2021', 'Published',
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=loadsubcategories(' + categories[i].id + ')><i class="icofont-edit text-success"></i></a>\
                        <button id='+ categories[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=deletecategory(' + categories[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )
            }
            table.draw();
            $('#pageHeadButton').html('<a href="#addcategory" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Categories</a>')
            $('#pageHeading').html('Main Categorie List')

        },
        error: function (jqXHR) {
        }
    });
}


$('#categoryform').submit(function (event) {
    event.preventDefault();
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
    var name = $('#name').val();
    var title = $('#title').val();
    var description = $('#description').val();

    data = {
        "name": name,
        "title": title,
        "description": description,
        csrfmiddlewaretoken: csrf_token1
    }
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/admincategories/",
        type: 'POST',
        dataType: "JSON",
        data: data,

        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Token ' + localStorage.getItem('token')); },
        success: function (response) {
            LoadCategories()
        },
        error: function (jqXHR) {
        }
    });
});


function deletecategory(id) {

    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/deletecategory/" + id,
        type: 'DELETE',
        dataType: "JSON",

        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('admin')); },
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

function loadsubcategories(id) {


    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/admincategories/" + id,
        type: 'GET',
        dataType: "JSON",

        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('admin')); },
        success: function (response) {
            hideforms();
            $('#addsubcategory').show()
            table = $('#myDataTable').DataTable();
            table
                .rows()
                .remove()
                .draw();
            table.columns(1).header().to$().text('Categories')
            table.columns(2).header().to$().text('Photo')
            table.columns.adjust().draw();
            console.log(response['subcategories'])
            const subcategories = response['subcategories'];
            for (let i = 0; i < subcategories.length; i++) {

                table.row.add([subcategories[i].id, subcategories[i].name,
                '<img src="' + subcategories[i].image['extrsmall_square_crop'] + '">', 'Published',
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=loadsubsubcategories(' + subcategories[i].id + ')><i class="icofont-edit text-success"></i></a>\
                        <button id='+ subcategories[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=deletesubcategory(' + subcategories[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )

            }
            table.draw();
            hideforms();
            $('#addsubcategory').show()
            $('#subcatorder').val(subcategories.length + 1)
            $('#categoryID').val(id)
            $('#pageHeadButton').html('<a href="#addsubcategory" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Sub Categories</a>')
            $('#pageHeading').html(response['name'])
            return 0;

        },
        error: function (jqXHR) {
        }
    });


}


$('#subcategoryform').submit(function (event) {
    event.preventDefault();
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData(document.getElementById("subcategoryform"));
    formData.append("image", $("#subcatimage")[0].files[0]);
    formData.append("name", $("#subcatname").val());
    formData.append("order", $("#subcatorder").val());
    formData.append("category", $("#categoryID").val());
    formData.append("csrfmiddlewaretoken", csrf_token1);
    data = formData

    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/subcategories/",
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Token ' + localStorage.getItem('token')); },
        success: function (response) {
            loadsubcategories($("#categoryID").val())
        },
        error: function (jqXHR) {
            console.log(JSON.stringify(jqXHR))
        }

    });
});


function deletesubcategory(id) {

    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/deletesubcategory/" + id,
        type: 'DELETE',
        dataType: "JSON",

        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('admin')); },
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

function loadsubsubcategories(id) {

    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/subcategories/" + id,
        type: 'GET',
        dataType: "JSON",

        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('admin')); },
        success: function (response) {
            console.log(response)
            hideforms();
            $('#addsubsubcategory').show()
            table = $('#myDataTable').DataTable();
            table
                .rows()
                .remove()
                .draw();
            table.columns(1).header().to$().text('Sub Categories')
            table.columns(2).header().to$().text('Photo')
            table.columns.adjust().draw();
            console.log(response['subsubcategories'])
            const subsubcategories = response['subsubcategories'];
            for (let i = 0; i < subsubcategories.length; i++) {

                table.row.add([subsubcategories[i].id, subsubcategories[i].name,
                '<img src="' + subsubcategories[i].image['extrsmall_square_crop'] + '">', 'Published',
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=loadproducts(' + subsubcategories[i].id + ')><i class="icofont-edit text-success"></i></a>\
                        <button id='+ subsubcategories[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=deletesubsubcategory(' + subsubcategories[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )

            }
            table.draw();
            hideforms();
            $('#addsubsubcategory').show()
            $('#subcatorder').val(subsubcategories.length + 1)
            $('#subcategoryID').val(id)
            $('#pageHeadButton').html('<a href="#addsubcategory" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Sub Categories</a>')
            $('#pageHeading').append('> ' + response['name'] + '>')
            return 0;

        },
        error: function (jqXHR) {
        }
    });


}

$('#subsubcategoryform').submit(function (event) {
    event.preventDefault();
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData(document.getElementById("subsubcategoryform"));
    formData.append("image", $("#subsubcatimage")[0].files[0]);
    formData.append("name", $("#subsubcatname").val());
    formData.append("order", $("#subsubcatorder").val());
    formData.append("subcategory", $("#subcategoryID").val());
    formData.append("csrfmiddlewaretoken", csrf_token1);
    data = formData

    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminsubsubcategories/",
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Token ' + localStorage.getItem('token')); },
        success: function (response) {
            loadsubsubcategories($("#subcategoryID").val())
        },
        error: function (jqXHR) {
            console.log(JSON.stringify(jqXHR))
        }

    });
});


function deletesubsubcategory(id) {

    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/deletesubsubcategory/" + id,
        type: 'DELETE',
        dataType: "JSON",

        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('admin')); },
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



function loadproducts(id) {

    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminsubsubcategories/" + id,
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
            console.log(response['products'])
            const products = response['products'];
            for (let i = 0; i < products.length; i++) {

                table.row.add([products[i].id, products[i].name,
                '<img src="' + products[i].image['extrsmall_square_crop'] + '">', 'Published',
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=loadproducts(' + products[i].id + ')><i class="icofont-edit text-success"></i></a>\
                        <button id='+ products[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=deletesubsubcategory(' + products[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )

            }
            table.draw();
            hideforms();
            $('#addproduct').show()
            $('#productorder').val(products.length + 1)
            $('#subsubcategoryID').val(id)
            $('#pageHeadButton').html('<a href="#addsubcategory" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Sub Categories</a>')
            $('#pageHeading').append('> ' + response['name'] + '>')
            return 0;

        },
        error: function (jqXHR) {
        }
    });


}




$('#productform').submit(function (event) {
    event.preventDefault();
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData(document.getElementById("subsubcategoryform"));
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
        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Token ' + localStorage.getItem('token')); },
        success: function (response) {
            loadproducts($("#subsubcategoryID").val())
        },
        error: function (jqXHR) {
            console.log(jqXHR.responseText)
        }

    });
});
