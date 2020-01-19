var username = 'gazal'
    var password = 'qwerty123'
    var api_url = "/api/"
    var auth_token = 'Bearer ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc5NTA5Mzk2LCJqdGkiOiI4Nzk3Y2M4NzE1NDc0ZGRjOGFjNTk3NzcyZDIyZjNiYSIsInVzZXJfaWQiOjF9.Ua1mbT9dHJH0Vanloo-_mb0jlYpsJ3UM0dn_mSzGvKc'
    
    
function add_item(store_id, item_id, amount){
    var quantity = $(`#quantity_${store_id}${item_id}`).val();
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
            quantity: quantity
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

function quantity_change(item_id, store_id, unit_price){
    var quantity = $(`#quantity_${store_id}${item_id}`).val();
    console.log(unit_price * quantity)
    $(`#price_${store_id}${item_id}`).html((unit_price * quantity).toFixed(2));

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
                            <div class="row">
                                <div class="col-lg-6 col-md-6 col-sm-12">
                                    <h4>${elem.name}</h4>
                                </div>
                                <div class="col-lg-6 col-md-6 col-sm-12">
                                    <span class="amount_payable">Rs. <span id=store_${elem.id}>${elem.outstanding_amount}</span></span>
                                </div>
                            </div>
                            <table class="table mt-30"><tbody>`
                    
                elem.items.forEach(function(item, index){
                    item_name = item.name;
                    item_price = item.price
                    single_store_html = single_store_html + `
                    <tr>
                        <td style="width: 70%">${item_name}</td>
                        <td id=price_${elem.id}${item.id} style="width: 10%">${item_price}</td>
                        <td style="width: 10%">
                            <div class="qty mt-5">
                                <input type="number" class="count" id=quantity_${elem.id}${item.id} name="qty" value="1" onchange="quantity_change(${item.id}, ${elem.id}, ${item.price})">
                            </div>
                        </td>
                        <td style="width: 10%">
                            <button type="button" class="btn btn-success" onclick="add_item(${elem.id}, ${item.id}, ${item.price})">Purchase</button>
                        </td>
                    </tr>`
                })
                single_store_html = single_store_html + `</tbody></table></div></div></div>`
            });
            $(".shops_listing").html(single_store_html)
        }
    })
});