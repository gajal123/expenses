var api_url = "/api/"
var store_names = []

function unfollow_store(){
    $.ajax({
        url: api_url + `stores/${store_id}/`,
        contentType: "application/json",
        method: "PATCH",
        headers: {
            'Authorization': auth_token
        },
        data: JSON.stringify({
            remove_user: 1
        }),
        success: function(response){
            console.log(response);
            var url = "/stores/";
            location.href = url;

    location.href = url;
        }
    })
}

function add_store_info(store){
    console.log(store_id)
    $(".shop-title").html(store.name);
    $("#follower_number").html(`${store.followed_by.length} follower(s)`)
    $(".shop_address").html("Location: " + store.address)
}


$(document).ready(function(){
    $.ajax({
        url: api_url + `stores/${store_id}`,
        contentType: "application/json",
        method: 'GET',headers: {
            'Authorization': auth_token
        },

        success: function(response){
            store_info = response;
            add_store_info(store_info)

        }
    });

})