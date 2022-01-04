$(document).ready(function () {
    LoadOptions()
});
function LoadOptions() {
    var url = window.location.href;
    var params = url.split('/');
    id = params[params.length - 1]

    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminproducts/" + id,
        type: 'GET',
        dataType: "JSON",

        success: function (response) {
            table = $('#myDataTableListOptions').DataTable();
            table
                .rows()
                .remove()
                .draw();
            table.draw();
            table.columns(1).header().to$().text('Options')
            table.columns(2).header().to$().text('Photo')
            table.columns.adjust().draw();
            const options = response['options'];
            for (let i = 0; i < options.length; i++) {

                table.row.add(['<div onclick=loadsizes(' + options[i].id + ')>' + options[i].id + '</div>', '<div onclick=loadsizes(' + options[i].id + ')>' + options[i].color + '</div>',
                '<img src="' + options[i].image_one['extrsmall_square_crop'] + '">', 'Published',
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=editoption(' + options[i].id + ')><i class="icofont-edit text-success"></i></a>\
                        <button id='+ options[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=deleteoption(' + options[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )
            }
            table.draw();
            $('#optionorder').val(options.length + 1)
            $('#productID').val(id)
            $('#productName').val(response['name'])
            $('#pageHeadButton').html('<a href="#addproduct" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Product</a>')
            $('#pageHeading').html('<a href="#" onclick=loadproducts(' + $("#subsubcategoryID").val() + ')>' + $("#subsubcategoryName").val() + '</a> ' + '<a href="#" onclick=loadoptions(' + $("#productID").val() + ')>' + $("#productName").val() + '</a>')

        },
        error: function (jqXHR) {
        }
    });

}



$('#optionform').submit(function (event) {
    event.preventDefault();
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData(document.getElementById("optionform"));
    formData.append("image_one", $("#optionimageone")[0].files[0]);
    formData.append("image_two", $("#optionimagetwo")[0].files[0]);
    formData.append("image_three", $("#optionimagethree")[0].files[0]);
    formData.append("name", $("#optionname").val());
    formData.append("colorhash", $("#optioncolorhash").val());
    formData.append("color", $("#optioncolor").val());
    formData.append("order", $("#optionorder").val());
    formData.append("size", $("#optionsize").val());
    formData.append("stock", $("#optionstock").val());
    formData.append("product", $("#productID").val());
    formData.append("csrfmiddlewaretoken", csrf_token1);
    data = formData

    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminoptions/",
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,

        success: function (response) {
            
            $('#sizes').find('tr').each(function (i, el) {

                size = $(this).find("td:eq(0) input[type='text']").val();
                stock = $(this).find("td:eq(1) input[type='text']").val();
                data = {
                    "stock": stock,
                    "size": size,
                    "option": response.id
                }
                $.ajax({
                    url: "http://127.0.0.1:8000/stockapi/sizeslist/",
                    type: 'POST',
                    data: data,
                    dataType: "JSON",
                    data: data,

                    success: function (response) {
                        $('#optionform').get(0).reset()
$("img").attr("src","https://dummyimage.com/150x200.gif")
                    },
                    error: function (jqXHR) {
                        console.log(jqXHR.responseText)
                    }

                });
            }
            );
            LoadOptions()
        },
        error: function (jqXHR) {
            console.log(jqXHR.responseText)
        }

    });
});


function editoption(id) {
    window.location = "http://127.0.0.1:8000/stocks/editoptions/" + id;
}
function deleteoption(id) {
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
                    url: "http://127.0.0.1:8000/stockapi/deleteoption/" + id,
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

$("#optionimageone").change(function () {
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#imageone').attr('src', e.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    }
});
$("#optionimagetwo").change(function () {
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#imagetwo').attr('src', e.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    }
});


$("#optionimagethree").change(function () {
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#imagethree').attr('src', e.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    }
});

function loadsizes(id) {
    window.location = "http://127.0.0.1:8000/stocks/listsizes/" + id
}




$(document).on('click', '#addRow', function () {
    var html = '';
    html += `<tr>
                <td><input type="text" class="form-control" placeholder="Size"></td>
                <td><input type="text" class="form-control" placeholder="Stock"></td>
                <td><i class="icofont-plus me-2 fs-6" id="addRow"></i></td>
                <td><i class="icofont-minus me-2 fs-6" id="removeRow"></i></td>
            </tr>`;

    $('#sizes').append(html);
});
$(document).on('click', '#removeRow', function () {

    $(this).closest('tr').remove();
});