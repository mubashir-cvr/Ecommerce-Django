$(document).ready(function () {
    LoadBrands()
});


function LoadBrands() {
    $('#addcategory').show()
    table = $('#myDataTable').DataTable();
    table
        .rows()
        .remove()
        .draw();
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/brandlist/",
        type: 'GET',
        dataType: "JSON",


        success: function (response) {
            const brands = JSON.parse(JSON.stringify(response));
            console.log(brands)
            for (let i = 0; i < brands.length; i++) {

                table.row.add(['<div onclick=loadsubbrands(' + brands[i].id + ',"' + brands[i].name + '")>' + brands[i].id + '</div>', '<div onclick=loadsubbrands(' + brands[i].id + ',"' + brands[i].name + '")>' + brands[i].name + '</div>',
                '<div onclick=loadsubbrands(' + brands[i].id + ',"' + brands[i].name + '")>March 13, 2021</div>',brands[i].is_popular,
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=editbrands(' + brands[i].id + ',"' + brands[i].name + '")><i class="icofont-edit text-success"></i></a>\
                        <button id='+ brands[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=deletecategory(' + brands[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )
            }
            table.draw();
            $('#pageHeadButton').html('<a href="#addcategory" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add brands</a>')
            $('#pageHeading').html('<a href="#" onclick="LoadBrands()">Brand List</a>')

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
        url: "http://127.0.0.1:8000/stockapi/brandlist/",
        type: 'POST',
        dataType: "JSON",
        data: data,


        success: function (response) {
            $('#categoryform').get(0).reset()
            $("img").attr("src", "")
            LoadBrands()
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
                    url: "http://127.0.0.1:8000/stockapi/deletecategory/" + id,
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
function loadsubbrands(id, name) {
    // window.location = "http://127.0.0.1:8000/stocks/listsubbrands/" + id + "/" + name
}



