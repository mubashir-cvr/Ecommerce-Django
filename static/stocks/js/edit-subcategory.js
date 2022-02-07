$(document).ready(function () {
    var url      = window.location.href;
    var params = url.split('/');
    var id=params[params.length-1]
    $('#final_msg').hide()
    Loadsubcategories(id)
});


function Loadsubcategories(id){
    $.ajax({
        url: "/stockapi/subcategories/"+id,
        type: 'GET',
        
        success: function (response) {
            console.log(response)
            $('#imageone').attr("src",response.image.original)
            $('#subcatname').val(response.name)
            $('#subcatorder').val(response.order)
            $('#subcatID').val(response.id)
            $('#catID').val(response.category)
            $('#nummberofproducts').html(response.subsubcategories.length)
            for(let i=0;i<response.subsubcategories.length;i++){
                $('#subsubcategoryrows').append(
                    `
                    <tr>
                    <td>`+response.subsubcategories[i].id+`</td>
                    <td>`+response.subsubcategories[i].name+`</td>
                    <td>Published</td>
                    </tr>
                    `
                )
            }
        },
        error: function (jqXHR) {
            console.log(JSON.stringify(jqXHR))
        }

    });

}

$('#editsubcategory').submit(function (event) {
    event.preventDefault()
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
    
    var formData = new FormData(document.getElementById("editsubcategory"));
    
    formData.append("name", $("#subcatname").val());
    formData.append("order", $("#subcatorder").val());
    formData.append("category", $("#catID").val());
    if(document.getElementById("dropify-event").files.length != 0 ){
        formData.append("image", $("#dropify-event")[0].files[0]);
    }
    formData.append("csrfmiddlewaretoken", csrf_token1);
    data = formData
    id=$('#subcatID').val()
    $.ajax({
        url: "/stockapi/subcategories/"+id+"/",
        type: 'PATCH',
        data: formData,
        processData: false,
        contentType: false,
        
        success: function (response) {
            
            $('#editsubcategory').get(0).reset()
                $('#final_msg').fadeIn().delay(1000).fadeOut();
$("img").attr("src","https://dummyimage.com/150x200.gif")
            Loadsubcategories(id)
        },
        error: function (jqXHR) {
            console.log(JSON.stringify(jqXHR))
        }

    });
});

$("#dropify-event").change(function () {
    $('#submitbutton').show()
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#imageone').attr('src', e.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    }
});
