$(document).ready(function () {
    $('#final_msg').hide()
    Loadsubcategories()
});
function Loadsubcategories(){
    var url      = window.location.href;
    var params = url.split('/');
    $.ajax({
        url: "/stockapi/admincategories/"+params[params.length-2],
        type: 'GET',
        dataType: "JSON",

        
        success: function (response) {
            table = $('#myDataTableSubCategory').DataTable();
            table
                .rows()
                .remove()
                .draw();
            table.draw();
            table.columns(1).header().to$().text('Categories')
            table.columns(2).header().to$().text('Photo')
            table.columns.adjust().draw();
            console.log(response['subcategories'])
            const subcategories = response['subcategories'];
            console.log(subcategories)
            for (let i = 0; i < subcategories.length; i++) {

                table.row.add(['<div onclick=loadsubsubcategories(' +subcategories[i].id +')>'+subcategories[i].id+'</div>','<div onclick=loadsubsubcategories(' +subcategories[i].id +')>'+subcategories[i].name+'</div>',
                '<img src="' + subcategories[i].image['extrsmall_square_crop'] + '">', '<div onclick=loadsubsubcategories(' +subcategories[i].id +')>Published</div>',
                ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a class="btn btn-outline-secondary" onclick=editsubsubcategories('+subcategories[i].id+')><i class="icofont-edit text-success"></i></a>\
                        <button id='+ subcategories[i].id + ' type="button" class="btn btn-outline-secondary deleterow" onclick=deletesubcategory(' + subcategories[i].id + ')><i class="icofont-ui-delete text-danger"></i></button></div>'
                ]
                )

            }
            table.draw();
            $('#subcatorder').val(subcategories.length + 1)
            $("#categoryID").val(params[params.length-2])
            $('#categoryName').val(response['name'])
            $('#pageHeadButton').html('<a href="#addsubcategory" class="btn btn-primary py-2 px-5 btn-set-task w-sm-100"><i class="icofont-plus-circle me-2 fs-6"></i> Add Categories</a>')
            $('#pageHeading').html('<a href="/listsubcategories/'+$('#categoryID').val()+'/'+$('#categoryName').val()+'">'+$('#categoryName').val()+'</a>')
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
        url: "/stockapi/subcategories/",
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        
        success: function (response) {
            $('#subcategoryform').get(0).reset()
                $('#final_msg').fadeIn().delay(1000).fadeOut();
$("img").attr("src","https://dummyimage.com/150x200.gif")
            Loadsubcategories();
        },
        error: function (jqXHR) {
            console.log(JSON.stringify(jqXHR))
        }

    });
});


function deletesubcategory(id) {
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
        url: "/stockapi/deletesubcategory/" + id,
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


function loadsubsubcategories(id) {
    window.location="/listsubsubcategories/"+id
}

function editsubsubcategories(id){
    window.location="/editsubcategory/"+id

}

$("#subcatimage").change(function () {
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#imageone').attr('src', e.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    }
});