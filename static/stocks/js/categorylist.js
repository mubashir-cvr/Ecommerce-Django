$(document).ready(function () {
    LoadCategories()
});


function LoadCategories() {
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
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=loadsubcategories(' + categories[i].id +',"'+ categories[i].name + '")><i class="icofont-edit text-success"></i></a>\
                        <button id='+ categories[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=deletecategory(' + categories[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )
            }
            table.draw();
            $('#pageHeadButton').html('<a href="#addcategory" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Categories</a>')
            $('#pageHeading').html('<a href="#" onclick="LoadCategories()">Categorie List</a>')

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
function loadsubcategories(id,name) {
    window.location="http://127.0.0.1:8000/stocks/listsubcategories/"+id+"/"+name
}




