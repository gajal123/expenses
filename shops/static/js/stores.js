var username = 'gazal'
    var password = 'qwerty123'
    var api_url = "/api/"
    var auth_token = 'Bearer ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc5NTA5Mzk2LCJqdGkiOiI4Nzk3Y2M4NzE1NDc0ZGRjOGFjNTk3NzcyZDIyZjNiYSIsInVzZXJfaWQiOjF9.Ua1mbT9dHJH0Vanloo-_mb0jlYpsJ3UM0dn_mSzGvKc'
    
    
function add_item(store_id, item_id, amount){
    $.ajax({
        url: api_url + "purchase/",
        contentType: "application/json",
        headers: {
            "Authorization": auth_token
        },
        data: JSON.stringify({
            store: store_id,
            item: item_id,
            amount: amount,
            quantity: 1
        }),
        dataType: "json",
        type: "POST",
        success: function(result){

            console.log(result.outstanding_amount)
            $(`#store_${store_id}`).html(result.outstanding_amount);
        },
        error: function(error){
            console.log(error);
        }
    })
}

$(document).ready( function(){

    $.ajax({
        url: api_url + 'user_stores',
        contentType: "application/json",
        dataType: "json",
        headers: {
            'Authorization': auth_token
        },
        method: 'GET',
        success: function(result){
            console.log(result);
            var single_store_html = ``
            result.forEach(function(elem, index){
                var store_id = `store_${elem.id}`
                single_store_html = single_store_html + 
                `<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
		            <div class="box-customn">
                        <div class="info-area">
                            <h3>${elem.name}</h3>
                            Amount  Payable: <span id=store_${elem.id}>${elem.outstanding_amount}</span>
                            <table class="table mt-30"><tbody>`
                        // <p>${elem.city}</p>
                        // <h4>Rs. 11,250.00</h4>
                    
                elem.items.forEach(function(item, index){
                    item_name = item.name;
                    item_price = item.price
                    single_store_html = single_store_html + `
                    <tr>
                        <td>${item_name}</td>
                        <td>${item_price}</td>
                        <td><a class="add" onclick="add_item(${elem.id}, ${item.id}, ${item.price})" title="Add" data-toggle="tooltip"><i class="fa fa-plus" aria-hidden="true"></i></a></td>
                        <td></td>
                    </tr>`
                })
                single_store_html = single_store_html + `</tbody></table></div></div></div>`
            });
            $(".shops_listing").html(single_store_html)
        }
    })
});