$(document).ready(function(){
    LoadPage()
});
function LoadPage(){
    table = $('#myDataTable').DataTable();
            $.ajax({
                url: "http://127.0.0.1:8000/stockapi/admincategories/",
                type: 'GET',
                dataType: "JSON",

                beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Token ' + localStorage.getItem('token')); },
                success: function (response) {
                    const categories = JSON.parse(JSON.stringify(response));
                    for(let i = 0; i < categories.length; i++){
                        console.log()
                    var html=''
                    html=`<tr>
                    <td><strong>`+categories[i].id+`</strong></td>
                    <td>`+categories[i].name+`</td>
                    <td>March 13, 2021</td>
                    <td><span class="badge bg-success">Published</span></td>
                    <td>
                    <div class="btn-group" role="group" aria-label="Basic outlined example">
                    <a href="categories-edit.html" class="btn btn-outline-secondary"><i class="icofont-edit text-success"></i></a>
                    <button type="button" class="btn btn-outline-secondary deleterow"><i class="icofont-ui-delete text-danger"></i></button>
                    </div>
                    </td></tr>`
                    table.row.add([categories[i].id,categories[i].name,
                        'March 13, 2021','Published',
                        ' <div class="btn-group" role="group" aria-label="Basic outlined example"><a href="categories-edit.html" class="btn btn-outline-secondary"><i class="icofont-edit text-success"></i></a>\
                        <button type="button" class="btn btn-outline-secondary deleterow"><i class="icofont-ui-delete text-danger"></i></button></div>'
                        ]
                        )
                    }
                    table.draw();
                  
                },
                error: function (jqXHR) {
                }
            });
        }
$('#categoryform').submit(function( event ) { 
    alert("Hi")
        var csrf_token1 = $('[name="csrfmiddlewaretoken"]').val();
        var profileCreated = $('#profileCreated').val();
        var name = $('#name').val();
       
        data = {
            "profileCreated": profileCreated,
            "name": name,
            "gender": gender,
            "community": community,
            "moblie": moblie,
            "preferredProfile": preferredProfile,
            "dateOfBirth": dateOfBirth,
            "relegion": relegion,
            "nationality": nationality,
            "height": height,
            "weight": weight,
            "martialStatus": martialStatus,
            "complexion": complexion,
            "ethnicGroup": ethnicGroup,
            "bodyType": bodyType,
            "physicalStatus": physicalStatus,
            "motherTongue": motherTongue,
            "fatherOccupation": fatherOccupation,
            "motherOccupation": motherOccupation,
            "brothers": brothers,
            "sisters": sisters,
            "financialStatus": financialStatus,
            "smoking": smoking,
            "drinking": drinking,
            "numberofChildresn": numberofChildresn,
            "numberofsiblings": numberofsiblings,
            "elderBrothers": elderBrothers,
            "marriedBrothers": marriedBrothers,
            "youngerSisters": youngerSisters,
            "marriedSisters": marriedSisters,
            "elderSister":elderSister,
            "yongerBrother":yongerBrother,
            "languagespoken": languagespoken,
            "whenmarry": whenmarry,
        }
        var total_siblings = parseInt(elderBrothers) + parseInt(marriedBrothers) + parseInt(youngerSisters) + parseInt(marriedSisters)+parseInt(elderSister)+parseInt(yongerBrother)
        if (parseInt(numberofsiblings) != 0 && parseInt(total_siblings) == 0) {
            return siblingError();
        }

        $.ajax({
            url: "http://127.0.0.1:8000/stockapi/admincategories/",
            type: 'POST',
            dataType: "JSON",
            data: data,

            beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Token ' + localStorage.getItem('token')); },
            success: function (response) {
                window.location.href = "http://127.0.0.1:8000/profilerB/"
            },
            error: function (jqXHR) {
                if (jqXHR.status == 400) {
                    var responseText = jQuery.parseJSON(jqXHR.responseText);
                    $('#emailwarning').html(responseText['non_field_errors']);
                } else {
                    $('#emailwarning').html("Unnexpected Error Occured ");
                }
            }
        });
    });