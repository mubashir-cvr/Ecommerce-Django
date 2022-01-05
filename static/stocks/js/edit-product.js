$(document).ready(function () {
    var url = window.location.href;
    var params = url.split('/');
    var id = params[params.length - 1]
    $('#final_msg').hide()
    LoadProducts(id)

});


function LoadProducts(id) {
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminproducts/" + id,
        type: 'GET',

        success: function (response) {
            console.log(response)
            $('#imageone').attr("src", response.image.original)
            $('#productname').val(response.name)
            $('#productorder').val(response.order)
            $('#productprice').val(response.price)
            $('#productID').val(response.id)
            $('#subsubcatID').val(response.subsubcategory)
            $('#nummberofproducts').html(response.options.length)
            for (let i = 0; i < response.options.length; i++) {
                $('#productrows').append(
                    `
                        <tr>
                        <td>`+ response.options[i].id + `</td>
                        <td>`+ response.options[i].color + `</td>
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

$('#editproduct').submit(function (event) {
    event.preventDefault()
    var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();

    var formData = new FormData(document.getElementById("editproduct"));
    formData.append("name", $("#productname").val());
    formData.append("order", $("#productorder").val());
    formData.append("price", $("#productprice").val());
    formData.append("subsubcategory", $("#subsubcatID").val());
    if (document.getElementById("dropify-event").files.length != 0) {
        formData.append("image", $("#dropify-event")[0].files[0]);
    }
    formData.append("csrfmiddlewaretoken", csrf_token1);
    data = formData
    id = $('#productID').val()
    $.ajax({
        url: "http://127.0.0.1:8000/stockapi/adminproducts/" + id + "/",
        type: 'PATCH',
        data: formData,
        processData: false,
        contentType: false,

        success: function (response) {
            
            $('#editproduct').get(0).reset()
                $('#final_msg').fadeIn().delay(1000).fadeOut();
            $("img").attr("src", "https://dummyimage.com/150x200.gif")
            LoadProducts(id)
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
