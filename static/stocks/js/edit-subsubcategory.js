$(document).ready(function () {
    var url      = window.location.href;
    var params = url.split('/');
    var id=params[params.length-1]
    $('#submitbutton').hide()
    Loadsubsubcategories(id)
   
});


function Loadsubsubcategories(id){
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminsubsubcategories/"+id,
        type: 'GET',
        
        success: function (response) {
            console.log(response)
            $('#imageone').attr("src",response.image.original)
            $('#subcatname').val(response.name)
            $('#subcatorder').val(response.order)
            $('#subsubcatID').val(response.id)
            $('#subcatID').val(response.subcategory)
            $('#nummberofproducts').html(response.products.length)
            for(let i=0;i<response.products.length;i++){
                $('#productrows').append(
                    `
                    <tr>
                    <td>`+response.products[i].id+`</td>
                    <td>`+response.products[i].name+`</td>
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

$('#editsubsubcategory').submit(function (event) {
    event.preventDefault()
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
    
    var formData = new FormData(document.getElementById("editsubsubcategory"));
    
    formData.append("name", $("#subsubcatname").val());
    formData.append("order", $("#subsubcatorder").val());
    formData.append("subcategory", $("#subcatID").val());
    if(document.getElementById("dropify-event").files.length != 0 ){
        formData.append("image", $("#dropify-event")[0].files[0]);
    }
    formData.append("csrfmiddlewaretoken", csrf_token1);
    data = formData
    id=$('#subsubcatID').val()
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/subcategories/"+id+"/",
        type: 'PATCH',
        data: formData,
        processData: false,
        contentType: false,
        
        success: function (response) {
            $('#submitbutton').hide()
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
$("#subcatname").change(function () {
    $('#submitbutton').show()
});
$("#subcatorder").change(function () {
    $('#submitbutton').show()
});