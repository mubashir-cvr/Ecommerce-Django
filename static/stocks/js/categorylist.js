$(document).ready(function () {
    $('#final_msg').hide()
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
        url: "/stockapi/admincategories/",
        type: 'GET',
        dataType: "JSON",


        success: function (response) {
            const categories = JSON.parse(JSON.stringify(response));
            for (let i = 0; i < categories.length; i++) {
                table.row.add(['<div onclick=loadsubcategories(' + categories[i].id + ',"test")>' + categories[i].id + '</div>', '<div onclick=loadsubcategories(' + categories[i].id + ',"test")>' + categories[i].name + '</div>',
                '<div onclick=loadsubcategories(' + categories[i].id + ',"test")>March 13, 2021', 'Published</div>',
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=editcategories(' + categories[i].id + ',"test")><i class="icofont-edit text-success"></i></a>\
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
        "description": "description",
        csrfmiddlewaretoken: csrf_token1
    }
    $.ajax({
        url: "/stockapi/admincategories/",
        type: 'POST',
        dataType: "JSON",
        data: data,


        success: function (response) {
            $('#categoryform').get(0).reset()
                $('#final_msg').fadeIn().delay(1000).fadeOut();
            $("img").attr("src", "")
            LoadCategories()
        },
        error: function (jqXHR) {
            console.log(jqXHR)
        }
    });
});


function deletecategory(id) {
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
                    url: "/stockapi/deletecategory/" + id,
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
            } else {
                swal("Safe");
            }
        });



}
function loadsubcategories(id, name) {
    window.location = "/listsubcategories/" + id + "/" + name
}




