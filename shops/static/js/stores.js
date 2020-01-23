var api_url = "/api/"
var auth_token = 'Bearer '
var store_names = []


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
            quantity: quantity,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        }),
        dataType: "json",
        type: "POST",
        success: function(result){

            console.log(result.outstanding_amount)
            $(`#store_balance_${store_id}`).html(result.outstanding_amount);
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
            store: store_id,
            csrfmiddlewaretoken: '{{ csrf_token }}'
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
            console.log(res);
        }
    })

}

function quantity_change(item_id, store_id, unit_price){
    var quantity = $(`#quantity_${store_id}${item_id}`).val();
    console.log(unit_price * quantity)
    $(`#price_${store_id}${item_id}`).html((unit_price * quantity).toFixed(2));

}

function toggle_open_payment(store_id){
    var x = document.getElementById(`pay_custom_amount_${store_id}`);
    if (x.style.display === "none") {
        x.style.display = "block";
      } else {
        x.style.display = "none";
      }
}

function make_payment(store_id){
    $(`#payment_error_${store_id}`).css("display", "none")
    var amount = $(`#payable_amount_${store_id}`).val()
    if(amount == ''){
        $(`#payment_error_${store_id}`).css("display", "block")
        return;
    }
    $.ajax({
        url: api_url + 'user_payment/',
        contentType: 'application/json',
        method: 'POST',
        headers: {
            'Authorization': auth_token
        },
        data: JSON.stringify({
            amount: amount,
            store: store_id,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        }),
        success: function(response){
            console.log(response)
            $(`#store_balance_${store_id}`).html(response.outstanding_amount);
            toggle_open_payment(store_id);

        }

    })
}

function get_all_stores(){
    $.ajax({
        url: api_url + 'stores',
        contentType: "application/json",
        dataType: "json",
        headers: {
            'Authorization': auth_token
        },
        method: 'GET',
        success: function(result){
            var single_store_html = ``
            result.forEach(function(store, index){
                var store_id = `store_${store.id}`
                var users = store.followed_by;
                store_names.push(store.name);
                if(users.indexOf(user_id) != -1){
                    single_store_html = single_store_html +
                    `<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                        <div class="box-customn">
                            <div class="info-area">
                                <div class="row">
                                    <div class="col-lg-6 col-md-6 col-sm-6">
                                        <h5><a href="/stores/1/?auth_token=${auth_token}">${store.name}</a></h5>
                                    </div>
                                    <div class="col-lg-6 col-md-6 col-sm-6">
                                        <div class="row" id="payment">
                                            <div class="col-lg-12 col-md-12 col-sm-12">
                                                <span class="amount_payable">Rs. <span id=store_balance_${store.id}>${store.outstanding_amount}</span>
                                                <button type="button" class="btn btn-success" onclick="toggle_open_payment(${store.id})">Make Payment</button>
                                                </span>
                                            </div>
                                            <div class="col-lg-12 col-md-12 col-sm-12">
                                                <div class="mt-30" id=pay_custom_amount_${store.id} style="display: none">
                                                    <input class="form-control" id=payable_amount_${store.id} placeholder="Amount">
                                                    <div id=payment_error_${store.id} style="color: red;display:none">Add Amount</div><br/>
                                                    <button type="button" class="btn btn-success" onclick="make_payment(${store.id})">Pay</button>
                                                </div>

                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <table class="table mt-30"><tbody>`

                    store.items.forEach(function(item, index){
                        if(item.followed_by.indexOf(user_id) != -1){
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
                        }
                    })
                    single_store_html = single_store_html +
                        `<tr>
                            <td style="width: 70%"><input class="form-control" id=new_item_name_${store.id} placeholder=" Item name"></td>
                            <td style="width: 10%"><input class="form-control"id=new_item_price_${store.id} placeholder="Price"></td>
                            <td style="width: 10%"></td>
                            <td style="width: 10%"><button type="button" class="btn btn-success" onclick="add_new_item(${store.id})">Add Item</button></td>

                        </tr>
                        <tr><td id=item_add_error_${store.id} style="color: red;visibility:hidden">Add Item name and Price</td></tr>`
                    single_store_html = single_store_html + `</tbody></table></div></div></div>`
                }
            });
            $(".shops_listing").html(single_store_html)
        }
    })
}

function add_new_store(){
    $("#store_add_error").css("visibility", "hidden");
    store_name = $("#new_shop_name").val();
    store_city = $("#new_shop_city").val();
    outstanding_amount = $("#new_shop_outstanding_amount").val();
    if(store_name == '' || store_city == ''){
        $("#store_add_error").css("visibility", "visible");
        return;
    }
    if(outstanding_amount == ''){
        outstanding_amount = 0;
    }
    $.ajax({
        url: api_url + 'stores/',
        contentType: 'application/json',
        headers: {
            'Authorization': auth_token
        },
        method: 'POST',
        data: JSON.stringify({
            name: store_name,
            city: store_city,
            address: store_city,
            item_name: 'test',
            item_price: 10,
            outstanding_amount: outstanding_amount,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        }),
        success: function(response){
            console.log(response);
            location.reload(true);

        },
        error: function(response){
            console.log(response);
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
            get_all_stores();
        }
    });
    $("#new_store").click(function(){
    $("#new_store").attr("disabled", true);
          var new_store_html = $(".shops_listing").html();
          new_store_html = `
                <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
		            <div class="box-customn">
                        <div class="info-area">
                            <div class="row">
                                <div class="col-lg-4 col-md-6 col-sm-12">
                                    <input class="form-control" id="new_shop_name" placeholder="Enter shop name">
                                </div>
                                <div class="col-lg-4 col-md-6 col-sm-12">
                                    <input class="form-control" id="new_shop_city" placeholder="Enter shop city">
                                </div>
                                <div class="col-lg-2 col-md-6 col-sm-12">
                                    <input class="form-control" id="new_shop_outstanding_amount" placeholder="Outstanding amount">
                                </div>
                                <div class="col-lg-2 col-md-6 col-sm-12">
                                    <button type="button" class="btn btn-success" onclick="add_new_store()">Add Store</button>
                                </div><br/><br/>
                                <div class="col-lg-12 col-md-16 col-sm-12">
                                    <div id="store_add_error" style="color:red; visibility: hidden"> Enter Shop name and city</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

          ` + new_store_html
          $(".shops_listing").html(new_store_html);
    })



});