var username = 'gazal'
var password = 'qwerty123'
var api_url = "/api/"
var auth_token = 'Bearer '

function purchase_item(store_id, item_id, amount){
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

function add_new_item(store_id){
    $(`#item_add_error_${store_id}`).css("visibility", "hidden");
    $(`#item_add_error_${store_id}`).html("Add Item name and Price");
    var item_name = $(`#new_item_name_${store_id}`).val();
    var item_price = $(`#new_item_price_${store_id}`).val();
    if(item_name == '' || item_price == ''){
        $(`#item_add_error_${store_id}`).css("visibility", "visible");
        return;
    }
    $.ajax({
        url: api_url + 'items/',
        contentType: 'application/json',
        dataType: "json",
        headers: {
            'Authorization': auth_token
        },
        method: 'POST',
        data: JSON.stringify({
            name: item_name,
            price: item_price,
            store: store_id
        }),
        success: function(result){
            if(result.error){
                console.log(result);
                $(`#item_add_error_${store_id}`).html(result['error']);
                $(`#item_add_error_${store_id}`).css("visibility", "visible");
            }
            else{
                location.reload(true);
            }
        },
        error: function(res){

        }
    })

}

function quantity_change(item_id, store_id, unit_price){
    var quantity = $(`#quantity_${store_id}${item_id}`).val();
    console.log(unit_price * quantity)
    $(`#price_${store_id}${item_id}`).html((unit_price * quantity).toFixed(2));

}

function get_user_stores(){
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
            result.forEach(function(store, index){
                var store_id = `store_${store.id}`
                single_store_html = single_store_html +
                `<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
		            <div class="box-customn">
                        <div class="info-area">
                            <div class="row">
                                <div class="col-lg-6 col-md-6 col-sm-12">
                                    <h4>${store.name}</h4>
                                </div>
                                <div class="col-lg-6 col-md-6 col-sm-12">
                                    <span class="amount_payable">Rs. <span id=store_${store.id}>${store.outstanding_amount}</span></span>
                                </div>
                            </div>
                            <table class="table mt-30"><tbody>`

                store.items.forEach(function(item, index){
                    item_name = item.name;
                    item_price = item.price
                    single_store_html = single_store_html + `
                    <tr>
                        <td style="width: 70%">${item_name}</td>
                        <td id=price_${store.id}${item.id} style="width: 10%">${item_price}</td>
                        <td style="width: 10%">
                            <div class="qty mt-5">
                                <input type="number" class="count" id=quantity_${store.id}${item.id} name="qty" value="1" onchange="quantity_change(${item.id}, ${store.id}, ${item.price})">
                            </div>
                        </td>
                        <td style="width: 10%">
                            <button type="button" class="btn btn-success" onclick="purchase_item(${store.id}, ${item.id}, ${item.price})">Purchase</button>
                        </td>
                    </tr>`
                })
                single_store_html = single_store_html +
                    `<tr>
                        <td><input id=new_item_name_${store.id} placeholder=" Item name"></td>
                        <td><input id=new_item_price_${store.id} placeholder="Price"></td>
                        <td></td>
                        <td><button type="button" class="btn btn-success" onclick="add_new_item(${store.id})">Add Item</button></td>

                    </tr>
                    <tr><td id=item_add_error_${store.id} style="color: red;visibility:hidden">Add Item name and Price</td></tr>`
                single_store_html = single_store_html + `</tbody></table></div></div></div>`
            });
            $(".shops_listing").html(single_store_html)
        }
    })
}

$(document).ready( function(){
    $.ajax({
        url: api_url + 'token/',
        contentType: "application/json",
        method: 'POST',
        data: JSON.stringify({
            username: username,
            password: password
        }),
        success: function(result){
            auth_token = auth_token + result.access;
            console.log(auth_token);
            get_user_stores()
        }
    });
//    $("#new_store").click(function(){
//        console.log('here');
//    })



});