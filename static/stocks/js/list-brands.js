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
        url: "https://voui.geany.website/stockapi/brandlist/",
        type: 'GET',
        dataType: "JSON",


        success: function (response) {
            const brands = JSON.parse(JSON.stringify(response));
            console.log(brands)
            for (let i = 0; i < brands.length; i++) {

                table.row.add(['<div onclick=loadsubbrands(' + brands[i].id + ',"' + brands[i].name + '")>' + brands[i].id + '</div>', '<div onclick=loadsubbrands(' + brands[i].id + ',"' + brands[i].name + '")>' + brands[i].name + '</div>',
                '<div onclick=loadsubbrands(' + brands[i].id + ',"' + brands[i].name + '")>March 13, 2021</div>',brands[i].is_popular,
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=editbrands(' + brands[i].id + ',"' + brands[i].name + '")><i class="icofont-edit text-success"></i></a>\
                        <button id='+ brands[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=deletebrand(' + brands[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
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


$('#brandform').submit(function (event) {
    event.preventDefault();
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
    var name = $('#brandName').val()
    var popular = ($('#Popular').is(
        ":checked"))
    console.log(name)
    data = {
        "name": name,
        "is_popular": popular,
        csrfmiddlewaretoken: csrf_token1
    }
    $.ajax({
        url: "https://voui.geany.website/stockapi/brandlist/",
        type: 'POST',
        data:data,
        dataType: "JSON",
        success: function (response) {
            $('#brandform').get(0).reset()
            LoadBrands()
        },
        error: function (jqXHR) {
            console.log(jqXHR)
        }
    });
});


function deletebrand(id) {
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
                    url: "https://voui.geany.website/stockapi/deletebrand/" + id,
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
    // window.location = "https://voui.geany.website/stocks/listsubbrands/" + id + "/" + name
}




