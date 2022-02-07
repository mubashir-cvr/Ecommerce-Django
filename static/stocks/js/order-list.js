$(document).ready(function(){
    $.ajax({
        url: "/stockapi/adminorders/",
        type: 'GET',
        dataType: "JSON",

        success: function (response) {
            console.log(response)
            table = $('#myDataTable').DataTable();
            table
                .rows()
                .remove()
                .draw();
            table.draw();
            
            const order = response;
            for (let i = 0; i < order.length; i++) {
                var payinfo="Payment Completed"
                if(order[i].has_paid==false){
                    payinfo="Pending"

                }
                table.row.add(['<div onclick=loadOrder(' + order[i].id + ')>' +order[i].id+ '</div>','<div onclick=loadOrder(' + order[i].id + ')>' + order[i].product.name + '</div>','<div onclick=loadOrder(' + order[i].id + ')>' + order[i].firstName + '</div>','<div onclick=loadOrder(' + order[i].id + ')>' + payinfo + '</div>','<div onclick=loadOrder(' + order[i].id + ')>' +order[i].amount+" "+order[i].currency,order[i].status+ '</div>'])
            }
            table.draw();
            

        },
        error: function (jqXHR) {
        }
    });
})

function loadOrder(id){
    window.location = "/orderdetails/" + id

}