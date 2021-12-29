$(document).ready(function () {
    Loadsubsubcategories()
});
function Loadsubsubcategories(){
    var url      = window.location.href;
    var params = url.split('/');
    id= params[params.length-1]
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/subcategories/" + id,
        type: 'GET',
        dataType: "JSON",

        beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('admin')); },
        success: function (response) {
            console.log(response)
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
            $('#addsubsubcategory').show()
            $('#subcatorder').val(subsubcategories.length + 1)
            $('#subcategoryID').val(id)
            $('#subcategoryName').val(response['name'])
            $('#pageHeadButton').html('<a href="#addsubsubcategory" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Sub Categories</a>')
            $('#pageHeading').html('<a href="#" onclick=loadsubcategories('+$("#categoryID").val()+')>'+$("#categoryName").val()+'</a>\
            >  '+'<a href="#" onclick=loadsubsubcategories('+$("#subcategoryID").val()+')>'+$("#subcategoryName").val()+'</a>')
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
            Loadsubsubcategories()
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
    
    window.location="http://127.0.0.1:8000/stocks/listproducts/"+id

}









