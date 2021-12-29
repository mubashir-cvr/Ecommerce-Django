$(document).ready(function () {
    Loadsubcategories()
});
function Loadsubcategories(){
    var url      = window.location.href;
    var params = url.split('/');
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/admincategories/"+params[params.length-2],
        type: 'GET',
        dataType: "JSON",

        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('admin')); },
        success: function (response) {
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
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=loadsubsubcategories('+subcategories[i].id+')><i class="icofont-edit text-success"></i></a>\
                        <button id='+ subcategories[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=deletesubcategory(' + subcategories[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )

            }
            table.draw();
            $('#subcatorder').val(subcategories.length + 1)
            $("#categoryID").val(params[params.length-2])
            $('#categoryName').val(response['name'])
            $('#pageHeadButton').html('<a href="#addsubcategory" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Categories</a>')
            $('#pageHeading').html('<a href="http://127.0.0.1:8000/stocks/listcategories">Categorie List</a>  >'+'<a href="#" onclick=loadsubcategories('+$("#categoryID").val()+')>'+ $('#categoryName').val()+'</a>')
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
            Loadsubcategories();
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
    window.location="http://127.0.0.1:8000/stocks/listsubsubcategories/"+id
}

