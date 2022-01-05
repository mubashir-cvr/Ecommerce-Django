$(document).ready(function () {
    $('#final_msg').hide()
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

        
        success: function (response) {
            console.log(response)
            table = $('#myDataTableSubSubCategory').DataTable();
            table
                .rows()
                .remove()
                .draw();
            table.draw();
            table.columns(1).header().to$().text('Sub Categories')
            table.columns(2).header().to$().text('Photo')
            table.columns.adjust().draw();
            console.log(response['subsubcategories'])
            const subsubcategories = response['subsubcategories'];
            for (let i = 0; i < subsubcategories.length; i++) {

                table.row.add(['<div onclick=loadproducts('+subsubcategories[i].id+')>'+subsubcategories[i].id+'</div>','<div onclick=loadproducts(' +subsubcategories[i].id +')>'+ subsubcategories[i].name+'</div>',
                '<img src="' + subsubcategories[i].image['extrsmall_square_crop'] + '">', '<div onclick=loadproducts('+subsubcategories[i].id+')>Published</div>',
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=editsubsubcategory(' + subsubcategories[i].id + ')><i class="icofont-edit text-success"></i></a>\
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
            $('#pageHeading').html( '<a href="#" onclick=loadsubsubcategories('+$("#subcategoryID").val()+')>'+$("#subcategoryName").val()+'</a>')
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
        
        success: function (response) {
            $('#subsubcategoryform').get(0).reset()
                $('#final_msg').fadeIn().delay(1000).fadeOut();
$("img").attr("src","https://dummyimage.com/150x200.gif")
            Loadsubsubcategories()
        },
        error: function (jqXHR) {
            console.log(JSON.stringify(jqXHR))
        }

    });
});


function deletesubsubcategory(id) {
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
        url: "http://127.0.0.1:8000/stockapi/deletesubsubcategory/" + id,
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
}else {
    swal("Safe");
}
});

}

function editsubsubcategory(id) {
    window.location="http://127.0.0.1:8000/stocks/editsubsubcategory/"+id

}


function loadproducts(id) {
    
    window.location="http://127.0.0.1:8000/stocks/listproducts/"+id

}

$("#subsubcatimage").change(function () {
    $('#submitbutton').show()
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#imageone').attr('src', e.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    }
});









