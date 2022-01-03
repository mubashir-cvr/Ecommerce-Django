    $(document).ready(function () {
        var url      = window.location.href;
        var params = url.split('/');
        var id=params[params.length-1]
        $('#submitbutton').hide()
        Loadoptions(id)
    
    });


    function Loadoptions(id){
        $.ajax({
            url: "http://127.0.0.1:8000/stockapi/adminoptions/"+id,
            type: 'GET',
            
            success: function (response) {
                console.log(response)
                $('#imageone').attr("src",response.image_one.original)
                $('#imagetwo').attr("src",response.image_two.original)
                $('#imagethree').attr("src",response.image_three.original)
                $('#productname').val(response.name)
                $('#optioncolor').val(response.color)
                $('#optioncolorhash').val(response.colorhash)
                $('#optionorder').val(response.order)
                $('#optionsize').val(response.size)
                $('#optionstock').val(response.stock)
                $('#OptionID').val(response.id)
                $('#productID').val(response.product)
            },
            error: function (jqXHR) {
                console.log(JSON.stringify(jqXHR))
            }

        });

    }

    $('#editoptionform').submit(function (event) {
        event.preventDefault()
        var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
        
        var formData = new FormData(document.getElementById("editoptionform"));
        formData.append("name", $("#productname").val());
        formData.append("order", $("#optionorder").val());
        formData.append("size", $("#optionsize").val());
        formData.append("product", $("#productID").val());
        formData.append("color", $("#optioncolor").val());
        formData.append("colorhash", $("#optioncolorhash").val());
        if(document.getElementById("optionimageone").files.length != 0 ){
            formData.append("image_one", $("#optionimageone")[0].files[0]);
        }
        if(document.getElementById("optionimagetwo").files.length != 0 ){
            formData.append("image_two", $("#optionimagetwo")[0].files[0]);
        }
        if(document.getElementById("optionimagethree").files.length != 0 ){
            formData.append("image_three", $("#optionimagethree")[0].files[0]);
        }
        formData.append("csrfmiddlewaretoken", csrf_token1);
        data = formData
        id=$('#OptionID').val()
        $.ajax({
            url: "http://127.0.0.1:8000/stockapi/adminoptions/"+id+"/",
            type: 'PATCH',
            data: formData,
            processData: false,
            contentType: false,
            
            success: function (response) {
                $('#submitbutton').hide()
                Loadoptions(id)
            },
            error: function (jqXHR) {
                console.log(JSON.stringify(jqXHR))
            }

        });
    });

    $("#optionimageone").change(function () {
        $('#submitbutton').show()
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imageone').attr('src', e.target.result);
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    $("#optionimagetwo").change(function () {
        $('#submitbutton').show()
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagetwo').attr('src', e.target.result);
            }
            reader.readAsDataURL(this.files[0]);
        }
    });
   
    $("#optionorder").change(function () {
        $('#submitbutton').show()
    });
    $("#optioncolor").change(function () {
        $('#submitbutton').show()
    });
    $("#optioncolorhash").change(function () {
        $('#submitbutton').show()
    });
    $("#optionsize").change(function () {
        $('#submitbutton').show()
    });

    $("#optionstock").change(function () {
        $('#submitbutton').show()
    });